import networkx as nx
import webbrowser

graph = nx.DiGraph()

graph.add_node(1, label="dasd")
graph.add_node(2, label="324dsf")
graph.add_edge(1, 2, link="")


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
        edgelist.append(
            {
                "from": u[0],
                "to": u[1],
                "label": u[2]['link']
            }
        )

    return nodelist, edgelist


def visualise(nodelist, edgelist):
    htmlbody = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>Network</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {{
                width: 600px;
                height: 400px;
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

    open('test.html', 'w', encoding='utf-8').write(htmlbody)
    webbrowser.open('test.html')


nodelist, edgelist = process_visgraph(graph)
visualise(nodelist, edgelist)
