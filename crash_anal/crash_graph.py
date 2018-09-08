from archs.arch import Arch
from crash_anal.crash_anal import CrashAnal
from crash_anal.checks import Checks
from graph.graph import Graph

import sys


class CrashGraph:

    def __init__(self, object, file_name):
        """" Initialized the object's internal data.
        Args:
            object: Crash object
            file_name: png output file name
        """
        self.r2_obj = object.r2_obj
        self.r2_dbg_obj = object.r2_dbg_obj
        self.r2_stand_obj = object.r2_stand_obj
        self.graph_obj = Graph()
        self.count = 1
        self.file_name = file_name


    def crash_graph(self):
        """ Graph generation """

        self.r2_stand_obj.analyze()
        self.arch_obj = Arch(self.r2_obj)

        self.r2_dbg_obj.debug_setenv("dbg.btdepth", "256")

        #afl
        func_list = self.r2_stand_obj.aflqj()

        if not func_list:
            print("No functions")
            sys.exit(-1)

        #set bps
        for function in func_list:
            self.r2_dbg_obj.debug_break(function)

        self.node_list = []
        self.range_list = []
        first = True

        while True:
            # continue
            self.r2_dbg_obj.debug_continue()

            get_info = self.r2_dbg_obj.debug_infoj()
            signal = get_info["signal"]

            self.r2_dbg_obj.debug_dmmSy()

            self.pc = self.arch_obj.get_reg("program_counter")
            self.pdj = self.r2_dbg_obj.debug_pdj_single(self.pc)
            bt = self.r2_dbg_obj.debug_dbt()

            # check access violation signal
            if Checks.check_signal(signal):
                regs = self.r2_dbg_obj.debug_registers()
                node_name = "crash_node"
                message = ""
                is_exploitable = False

                if self.pdj[0]["type"] == "invalid":
                    print("ERROR: Function crash_graph, the type is invalid!")
                    return False

                opcode = self.pdj[0]["opcode"]
                crash_address = self.pdj[0]["offset"]

                is_exploitable = CrashAnal.exploitable(signal, self.r2_dbg_obj)
                if is_exploitable:
                    exploitable_message = "PROBABLY EXPLOITABLE"
                    message = "crash details"
                else:
                    exploitable_message = "PROBABLY NOT EXPLOITABLE"
                    message = "details"

                label = "Exploitable: " + exploitable_message + " \n " + "crash instruction: \n" + str(hex(crash_address)) + " - " + str(opcode) + " \nbacktrace: \n " + bt + " \n " + "registers: \n" + regs + " \n "
                self.node = self.graph_obj.create_node(node_name, "green", label)
                self.node_list.append(self.node)

                # create edge
                try:
                    caller_address = bt.splitlines()[1].split()[1]
                except Exception as ex:
                    print("WARNING: caller address - backtrace error: %s" % ex)
                    caller_address = "0x0"

                self.create_edge(int(caller_address, 16), message)

                break

            if signal != "SIGTRAP":
                break

            if first:
                self.create_node("gold")
                first = False
                continue

            self.create_node("gold")

            try:
                caller_address = self.pdj[0]["xrefs"][0]["addr"]
            except Exception as ex:
                print("WARNING: caller address - xref not there: %s" % ex)
                try:
                    caller_address = bt.splitlines()[1].split()[1]
                except Exception as ex:
                    print("WARNING: caller address - backtrace erro: %s" % ex)
                    continue

            # create edge
            self.create_edge(caller_address, self.count)

        # create png
        self.graph_obj.create_png(self.file_name)

    def create_node(self, color):
        function_address = self.pdj[0]["fcn_addr"]
        func_address_end = self.pdj[0]["fcn_last"]
        r = range(function_address, func_address_end)
        self.range_list.append(r)
        func_name = self.pdj[0]["flags"][0]
        node_name = func_name
        label = func_name + " [ " + str(hex(function_address)) + " - " + str(hex(func_address_end)) + " ] "
        self.node = self.graph_obj.create_node(node_name, color, label)
        self.node_list.append(self.node)

    def create_edge(self, caller_address, label):
        for range_addr in self.range_list:
            if caller_address in range_addr:
                for single_node in self.node_list:
                    a = range_addr[0]
                    b = single_node.obj_dict["attributes"]["label"].split()[2]
                    if int(range_addr[0]) == int(b, 16):
                        self.graph_obj.create_edge(single_node, self.node, label)
                        self.count += 1
                        return
