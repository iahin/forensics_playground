from pyvis import network as net
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph3(networkx_graph, notebook=True, output_filename='graph.html', show_buttons=False,
                only_physics_buttons=False):
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.

    Valid node attributes include:
        "size", "value", "title", "x", "y", "label", "color".

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)

    Valid edge attributes include:
        "arrowStrikethrough", "hidden", "physics", "title", "value", "width"

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_edge)


    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter?
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network?
        only_physics_buttons: Show only buttons controlling physics of network?
    """

    # import

    # make a pyvis network
    pyvis_graph = net.Network(notebook=notebook)
    pyvis_graph.width = '1200px'
    pyvis_graph.height = '800px'
    pyvis_graph.directed = True
    pyvis_graph.toggle_physics(False)
    # for each node and its attributes in the networkx graph
    for node, node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(node, **node_attrs)
    #         print(node,node_attrs)

    # for each edge and its attributes in the networkx graph
    for source, target, edge_attrs in networkx_graph.edges(data=True):
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        if not 'title' in edge_attrs and 'ttp' in edge_attrs:
            # place at key 'value' the weight of the edge
            #edge_attrs['value'] = edge_attrs['weight']
            edge_attrs['title'] = edge_attrs['ttp']
        # add the edge
        pyvis_graph.add_edge(source, target, **edge_attrs)

    # turn buttons on
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=['physics'])
        else:
            pyvis_graph.show_buttons()

    # return and also save
    return pyvis_graph.show(output_filename)


def simple_plot_image(G, path):
    edge_labels = nx.get_edge_attributes(G, 'link')  # key is edge, pls check for your case
    formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in
                             edge_labels}
    plt.figure(figsize=(18, 18))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=formatted_edge_labels, pos=pos)
    plt.savefig(path)
