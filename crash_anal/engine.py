from archs.arch import Arch
from archs.instruction import Instruction
from crash_anal.term_colors import TermColors


class Engine:

    def __init__(self, r2_obj):
        self.r2_obj = r2_obj
        self.stopaddr = None
        self.bt = self.r2_obj.debug_dbt()
        self.arch_obj = Arch(self.r2_obj)
        self.term_colors = TermColors()
        self.pc_name = self.arch_obj.get_reg("program_counter")
        self.pdj = self.r2_obj.debug_pdj_single(self.pc_name)[0]
        self.pc = self.pdj["offset"]
        self.type = self.pdj["type"]
        if self.type != "invalid":
            self.instr = Instruction(self.r2_obj, self.pc_name)

    def print_crash_info(self):
        print(self.term_colors.bold() + "backtrace" + self.term_colors.reset())
        print(self.bt)
        print(self.term_colors.bold() + "registers" + self.term_colors.reset())
        print(self.r2_obj.debug_registers())

    def stack_overf_libc(self):
        libs = ["fortify_fail", "stack_chk_fail"]
        try:
            if libs[0] in self.bt or libs[1] in self.bt:
                stack_report = "Stack error - Generally it could be exploitable, due to suspicious functions in the backtrace"
                print(self.term_colors.red() + stack_report + self.term_colors.default())
                self.print_crash_info()
                return stack_report
            return False
        except Exception as ex:
            print("stack_overf_libc - error type: %s" % ex)
            return False

    def crash_on_pc(self):
        try:
            dinfo = self.r2_obj.debug_infoj()
            self.stopaddr = dinfo["stopaddr"]

            if self.type == "div":
                self.not_exploitable()
                return False

            if self.stopaddr == self.pc or self.type == "invalid":
                crash_on_pc_report = "Crash on PC - Generally it is exploitable, the PC could be tainted"
                print(self.term_colors.red() + crash_on_pc_report + self.term_colors.default())
                self.print_crash_info()
                return crash_on_pc_report
            return False
        except Exception as ex:
            print("crash_on_pc - error type: %s" % ex)
            return False

    def crash_on_branch(self):
        if self.type != "invalid":
            try:
                is_branch_instr = self.instr.is_branch_instr()
            except Exception as ex:
                print("crash_on_branch - error type: %s" % ex)
                return False

            if is_branch_instr:
                crash_on_branch_report = "Crash on branch instruction - Generally it is exploitable, the branch address could be tainted"
                print(self.term_colors.red() + crash_on_branch_report + self.term_colors.default())
                self.print_crash_info()
                return crash_on_branch_report
            return False
        return False

    def invalid_write(self):
        try:
            if self.type != "invalid":
                is_mem_write = self.instr.is_memory_write()
                if is_mem_write:
                    dest_address = self.instr.get_dest_address()
                    if dest_address and int(dest_address, 16) == self.stopaddr:
                        size = self.instr.write_size()
                        invalid_write_report = "Invalid write crash - Generally it is exploitable, the write value/address could be tainted"

                        if size:
                            print(self.term_colors.red() + invalid_write_report + " - Invalid write of size %d" % size + self.term_colors.default())
                        else:
                            print(self.term_colors.red() + invalid_write_report + "Invalid write" + self.term_colors.default())
                        self.print_crash_info()
                    return invalid_write_report
            return False
        except Exception as ex:
            print("invalid_write - error type: %s" % ex)
            return False

    def heap_error(self):

        suspicius_heap_functions = """free malloc calloc realloc""".split()

        try:
            for i in suspicius_heap_functions:
                if i in self.bt:
                    heap_report = "Heap error - Generally it could be exploitable, due to suspicious functions in the backtrace"
                    print(self.term_colors.red() + heap_report + self.term_colors.default())
                    self.print_crash_info()
                    return heap_report
            return False
        except Exception as ex:
            print("heap_error - error type: %s" % ex)
            return False

    def read_access_violation(self):
        """ Check if it is a read access violation, and if it could be exploitable
        :return: True if it could be exploitable
        """
        try:
            if self.type != "invalid":
                is_mem_read = self.instr.is_memory_read()
                if is_mem_read:
                    if self.instr.call_check(self.arch_obj.get_regs()):
                        uaf_report = "It could be just a read access violation, but after few instruction there is a suspicious call, and if the address could be controlled by an attacker, it could lead to code execution"
                        print(self.term_colors.red() + uaf_report + self.term_colors.default())
                        self.print_crash_info()
                        return uaf_report
                    return False
            return False
        except Exception as ex:
            print("read_access_violation - error type: %s" % ex)
            return False

    def not_exploitable(self):
        not_exploitable_report = "PROBABLY NOT EXPLOITABLE"
        print(self.term_colors.green() + not_exploitable_report + self.term_colors.default())
