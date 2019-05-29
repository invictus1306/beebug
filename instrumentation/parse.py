from graph.graph import Graph
import sys

class Parse:

    def __init__(self, input_file, filename, crash_desc):
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
        self.name_function = ""
        self.args_label = ""
        self.ret = ""
        self.signal = ""
        self.signal_num = ""
        self.args = []
        self.crash_desc = crash_desc

    def read_file(self):
        with open(self.input_file) as fp:
            line = fp.readline()
            while line:
                new_line = self.parse(line, fp)
                if new_line == None:
                    line = fp.readline()
                else:
                    line = new_line

        # create pdf
        self.graph_obj.create_pdf(self.filename)

    def parse(self, line, fp):
        if "[FUNC]" in line:
            self.parse_line(line, True)
            new_line = self.parse_addr(fp)
            return new_line
        elif "[NOFUNC]" in line:
            self.parse_line(line, False)
            new_line = self.parse_nosym(fp)
            return new_line
        elif "[ARG]" in line:
            new_line = self.parse_args(line, fp)
            self.generate_ret_args()
            return new_line
        elif "[RET]" in line:
            new_line = self.parse_ret(line, fp)
            self.generate_ret_args()
            return new_line
        elif "[CRASH]" in line:
            self.parse_crash(line)
            self.generate_crash()
        else:
            return None

    def parse_line(self, line, func):
        line = line.split(";")
        self.start_address = line[1]
        self.end_address = line[2]
        self.pc = line[3]
        if func:
            self.name_function = line[4]
        else:
            self.name_function = self.pc

    def parse_crash(self, line):
        line = line.split(";")
        self.signal_num = line [1]
        self.signal = line[2]
        self.pc = line[3]

    def parse_addr(self, fp):
        new_line = fp.readline()
        if "TAG" in new_line:
            self.parse_disass(new_line, fp)
            new_line = None

        if self.count < 60000:
            self.generate_graph(True)
        else:
            print("It is not possible to generate the graph! (In pydot.py the call subprocess.Popen never end)")
            sys.exit()
        return new_line

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
            new_line = None

        if self.count < 60000:
            self.generate_graph(False)
        else:
            print("It is not possible to generate the graph! (In pydot.py the call subprocess.Popen never end)")
            sys.exit()

        return new_line

    def parse_args(self, line, fp):
        line = line.split(";")
        self.wrap_function = line[1]
        self.pc = line[2]
        self.arg_num = line[3]
        arg = "Arg" + self.arg_num + ": " + line[5] + "\n"
        self.args.append(arg)
        new_line = fp.readline()
        if "DUMP" in new_line:
            new_line = new_line.split(";")
            arg = "DUMP: " + new_line[2] + "\n"
            self.args.append(arg)
            new_line = None
        return new_line

    def parse_ret(self, line, fp):
        line = line.split(";")
        self.wrap_function = line[1]
        self.pc = line[2]
        self.ret = " Return value: " + line[3] + "\n"
        new_line = fp.readline()
        if "DUMP" in new_line:
            new_line = new_line.split(";")
            ret = "DUMP: " + new_line[2] + "\n"
            self.ret += ret
            new_line = None
        return new_line


    def generate_ret_args(self):
        node_name = str(self.wrap_function)
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
        node_name = str(self.pc)

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
            self.graph_obj.create_node(node_id, color, label)
            self.last_node = node_id
            self.count = self.count + 1
        else:
            self.graph_obj.create_node(node_id, color, label)
            self.graph_obj.create_edge(self.last_node, node_id, self.count)
            self.count = self.count + 1
            self.last_node = node_id

    def generate_crash(self):
        node_name = str(self.pc)
        self.crash_desc += "\nCrash at: " + self.pc + "Signal: " + self.signal_num + " [" + self.signal + "]"

        self.graph_obj.create_node(node_name, "Red", self.crash_desc)
        self.graph_obj.create_edge(self.last_node, node_name, self.count)