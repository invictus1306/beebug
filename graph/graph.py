import pydot


class Graph:

    def __init__(self):
        """" Initialized the object's internal data.
        """
        self.graph = pydot.Dot(graph_type='digraph')

    def create_node(self, name, color=False, label=False):
        if label==False:
            label = name

        node = pydot.Node(name, style="filled", color=color, label=label, shape="box", fontname="Microsoft YaHei")
        self.graph.add_node(node)
        return node

    def create_edge(self, node_in, node_out, message):
        self.graph.add_edge(pydot.Edge(node_in, node_out, label=message, labelfontcolor="#009933", fontsize="12.0", color="blue"))

    def create_png(self, name):
        self.graph.write_png(name + '.png')