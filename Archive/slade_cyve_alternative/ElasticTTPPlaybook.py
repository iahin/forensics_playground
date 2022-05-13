import json
import os
from pathlib import Path

import networkx as nx
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from tqdm import tqdm

from lipe.LogMapper import LogMapper
from temp.pyviz_utils import process_visgraph, show_graph


class ElasticTTPPlaybookClass(LogMapper):

    def __init__(self, casefolder, caseid):
        super().__init__(casefolder, caseid)
        self.es_instance = Elasticsearch(http_auth=('sitslade', 'admin123'))
        self.index_name = caseid
        queriesfilepath = str(Path.joinpath(Path(__file__).resolve().parents[0], 'lookups', 'elastic_ttp_queries.json'))
        self.queriesobj = json.loads(open(queriesfilepath).read())

        self.schema_df = pd.read_csv(
            str(Path.joinpath(Path(__file__).resolve().parents[0], 'lookups', 'schema_eventid.csv')))
        self.evtx_graph = str(Path.joinpath(Path(self.cache), "evtx_graph.gpickle"))
        self.evtx_graph_plot = str(Path.joinpath(Path(self.cache), "evtx_graph.png"))
        self.evtx_graph_html = str(Path.joinpath(Path(self.cache), "evtx_graph.html"))
        self.graph_obj = None

    def deleteinstance(self):
        if self.es_instance.indices.exists(index=self.index_name):
            self.es_instance.indices.delete(index=self.index_name)

    def indexer(self, loglist):
        """Upload log to index"""
        for item in tqdm(loglist):
            self.es_instance.index(index=self.index_name, body=item)

    def search_wrapper(self, queryobj):
        searchContext = Search(using=self.es_instance, index=self.index_name)
        search_query = searchContext.query('query_string', query=queryobj)
        response = search_query.execute()

        if response.success():
            result = [d.to_dict() for d in search_query.scan()]
            if result:
                return result

    def search_all(self):
        logindexlist = []
        for item in self.queriesobj:
            querystring = item['query']
            if self.search_wrapper(querystring):
                logindexlist.append(item['id'])

        return logindexlist

    def search_ttp(self, ttpid):
        logindexlist = []
        for item in self.queriesobj:
            if ttpid in item['id']:
                querystring = item['query']
                if self.search_wrapper(querystring):
                    logindexlist.append(item['id'])

        return logindexlist

    def distribute_graph(self):
        """Init and populates any general links most commonly associated in logs"""
        loglist = self.readevtxlog()
        schema_df = pd.read_csv(
            str(Path.joinpath(Path(__file__).resolve().parents[0], 'lookups', 'schema_eventid.csv')))

        G = nx.DiGraph()
        for item in tqdm(loglist):

            graphlinks = schema_df.loc[schema_df['event_id'] == int(item['event_id'])]
            graphlinks = graphlinks.values.tolist()
            if graphlinks:
                sourceref = graphlinks[0][0]
                linkref = graphlinks[0][1]
                destref = graphlinks[0][2]
                if all(x in item for x in [sourceref, destref]):
                    G.add_edge(item[sourceref], item[destref], link=linkref, ttp="")

        self.graph_obj = nx.convert_node_labels_to_integers(G, label_attribute='label')
        self.store_graph()

    def distribute_all_ttp(self):
        """Detect and add TTP to case graph"""
        G = nx.read_gpickle(self.evtx_graph)

        for item in self.queriesobj:
            querystring = item['query']
            getquery = self.search_wrapper(querystring)

            if getquery:
                getquery = getquery[0]
                graphlinks = self.schema_df.loc[self.schema_df['event_id'] == int(getquery['event_id'])]
                graphlinks = graphlinks.values.tolist()

                if graphlinks:
                    sourceref = graphlinks[0][0]
                    linkref = graphlinks[0][1]
                    destref = graphlinks[0][2]
                    if all(x in getquery for x in [sourceref, destref]):  # for edges

                        get_src_node_num = \
                        [k for k, v in G.nodes(data=True) if v['label'] == os.path.basename(getquery[sourceref])][0]
                        get_dest_node_num = \
                        [k for k, v in G.nodes(data=True) if v['label'] == os.path.basename(getquery[destref])][0]
                        G[get_src_node_num][get_dest_node_num]['ttp'] = item['id']
                        print(G[get_src_node_num][get_dest_node_num]['ttp'])

        self.graph_obj = G
        self.store_graph()
        return

    def distribute_single_ttp(self, ttpid):
        """Detect and add TTP to case graph"""
        G = nx.read_gpickle(self.evtx_graph)

        for item in self.queriesobj:
            if ttpid in item['id']:
                querystring = item['query']
                getquery = self.search_wrapper(querystring)

                if getquery:
                    getquery = getquery[0]
                    graphlinks = self.schema_df.loc[self.schema_df['event_id'] == int(getquery['event_id'])]
                    graphlinks = graphlinks.values.tolist()

                    if graphlinks:
                        sourceref = graphlinks[0][0]
                        linkref = graphlinks[0][1]
                        destref = graphlinks[0][2]
                        if all(x in getquery for x in [sourceref, destref]):  # for edges
                            get_src_node_num = \
                                [k for k, v in G.nodes(data=True) if
                                 v['label'] == os.path.basename(getquery[sourceref])][0]
                            get_dest_node_num = \
                                [k for k, v in G.nodes(data=True) if v['label'] == os.path.basename(getquery[destref])][
                                    0]
                            G[get_src_node_num][get_dest_node_num]['ttp'] = item['id']

        self.graph_obj = G
        self.store_graph()

    def visualise_whole_graph(self):
        """View the entire graph"""
        G = nx.read_gpickle(self.evtx_graph)
        nodelist, edgelist = process_visgraph(G)
        show_graph(nodelist, edgelist, self.evtx_graph_html)

    def visualise_subgraph(self, ttp):
        """View only the specific narrowed down graph of the TTPs in question"""
        G = nx.read_gpickle(self.evtx_graph)
        print(G.edges(data=True))
        H = G.to_undirected()
        nodelist = []

        getnodes = [(u,v) for u, v, w in H.edges(data=True) if w['ttp'] == ttp]

        for row in getnodes:
            nodelist.extend(row)

        newnodelist = []
        for x in nodelist:
            for i in nx.single_source_shortest_path(H, x, cutoff=2).keys():
                newnodelist.append(i)

        K = G.subgraph(newnodelist)
        nodelist, edgelist = process_visgraph(K)
        show_graph(nodelist, edgelist, self.evtx_graph_html)

    def store_graph(self):
        nx.write_gpickle(self.graph_obj, self.evtx_graph)
        #simple_plot_image(self.graph_obj, self.evtx_graph_plot)
