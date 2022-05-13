import webbrowser

import matplotlib.pyplot as plt
import networkx as nx


def process_visgraph(G):
    nodelist = []
    edgelist = []

    for u in G.nodes(data=True):
        nodelist.append(
            {
                "id": u[0],
                "label": u[1]['label']
            }
        )

    for u in G.edges(data=True):
        if 'ttp' in u[2]:
            edgelist.append(
                {
                    "from": u[0],
                    "to": u[1],
                    "label": u[2]['ttp']
                }
            )
        else:
            edgelist.append(
                {
                    "from": u[0],
                    "to": u[1]
                }
            )

    return nodelist, edgelist


def show_graph(nodelist, edgelist, fileoutput):
    htmlbody = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>Network</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {{
                width: 1200px;
                height: 800px;
                border: 1px solid lightgray;
            }}
        </style>
    </head>

    <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            // create an array with nodes
            var nodes = new vis.DataSet({nodelist});

            // create an array with edges
            var edges = new vis.DataSet({edgelist});

            // create a network
            var container = document.getElementById("mynetwork");
            var data = {{
                nodes: nodes,
                edges: edges,
            }};
            var options = {{
                edges:{{
                    arrows: {{
                    to: {{
                        enabled: true,
                        }}
                    }}
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>

    </html>
    """.format(nodelist=nodelist, edgelist=edgelist)

    open(fileoutput, 'w', encoding='utf-8').write(htmlbody)
    webbrowser.open(fileoutput)


def simple_plot_image(G, path):
    edge_labels = nx.get_edge_attributes(G, 'link')  # key is edge, pls check for your case
    formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in
                             edge_labels}
    plt.figure(figsize=(18, 18))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=formatted_edge_labels, pos=pos)
    plt.savefig(path)
