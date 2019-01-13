from graph.graph import Graph
import sys

class Parse:

    def __init__(self, input_file, filename):
        """" Initialized the object's internal data.
        """
        self.input_file = input_file
        self.graph_obj = Graph()
        self.filename = filename
        self.count = 0
        self.disass = []
        self.last_node = ""
        self.start_address = ""
        self.end_address = ""
        self.pc = ""
        self.name_function = None
        self.args_label = ""
        self.ret = None
        self.args = []

    def read_file(self):
        with open(self.input_file) as fp:
            line = fp.readline()
            while line:
                self.parse(line, fp)
                line = fp.readline()

        # create pdf
        self.graph_obj.create_pdf(self.filename)

    def parse_line(self, line, func):
        line = line.split(";")
        self.start_address = line[1]
        self.end_address = line[2]
        self.pc = line[3]
        if func:
            self.name_function = line[4]
        else:
            self.name_function = self.pc

    def parse(self, line, fp):
        if "[FUNC]" in line:
            self.parse_line(line, True)
            self.parse_addr(fp)
        elif "[NOFUNC]" in line:
            self.parse_line(line, False)
            self.parse_nosym(fp)
        elif "[ARG]" in line:
            self.parse_args(line, fp)
            self.generate_ret_args()
        elif "[RET]" in line:
            self.parse_ret(line)
            self.generate_ret_args()
        else:
            return

    def parse_addr(self, fp):
        new_line = fp.readline()
        if "TAG" in new_line:
            self.parse_disass(new_line, fp)
        if self.count < 600:
            self.generate_graph(True)
        else:
            print("TIt is not possible to generate the graph! (In pydot.py the call subprocess.Popen never end)")
            sys.exit()

    def parse_disass(self, line, fp):
        self.disass = []
        self.bb_start = line.split()[1]

        while "END" not in line:
            line = fp.readline()
            a = line[52:]
            self.disass.append(a)

        fp.readline()

    def parse_nosym(self, fp):
        new_line = fp.readline()
        if "TAG" in new_line:
            self.parse_disass(new_line, fp)
        if self.count < 600:
            self.generate_graph(False)
        else:
            print("It is not possible to generate the graph! (In pydot.py the call subprocess.Popen never end)")
            sys.exit()

    def parse_args(self, line, fp):
        line = line.split(";")
        self.wrap_function = line[1]
        arg = "Arg: " + line[3] + "\n"
        self.args.append(arg)
        line = fp.readline()
        line = line.split(";")
        while "ARG" in line:
            arg = "Arg: " + line[3] + "\n"
            self.args.append(arg)

    def parse_ret(self, line):
        line = line.split(";")
        self.wrap_function = line[1]
        self.ret = "Return value: " + line[2]

    def generate_ret_args(self):
        node_name = self.wrap_function
        color = "Orange"

        if not self.args_label:
            self.args_label = "Function: " + self.wrap_function + " [ " + self.start_address + " - " + self.end_address + " ] \n"

            if self.args:
                self.args_label += "".join(self.args)
                self.args =[]
        if self.ret:
            self.args_label += "\nFunction: " + self.wrap_function + self.ret
            self.ret = None
            node_id = node_name
            self.graph_obj.create_node(node_id, color, self.args_label)
            self.args_label = ""

    def generate_graph(self, no_sym):
        color = "Green"
        label = ""
        node_name = self.pc

        if no_sym:
            label += self.name_function
        else:
            label = "BB"

        label += " [ " + self.start_address + " - " + self.end_address + " ] "
        label += "\n PC: " + self.pc + "\n"

        if self.disass:
            label += "".join(self.disass)
            self.disass = []
            color = "yellow"

        node_id = node_name

        if self.count == 0: # first node
            self.node = self.graph_obj.create_node(node_id, color, label)
            self.last_node = self.node
            self.count = self.count + 1
        else:
            self.node = self.graph_obj.create_node(node_id, color, label)
            self.graph_obj.create_edge(self.last_node, self.node, self.count)
            self.count = self.count + 1
            self.last_node = self.node
