import re


class Instruction:

    def __init__(self, r2_obj, pc):
        """ Initialized the object's internal data """
        self.r2_obj = r2_obj
        self.is_pointer = False
        self.first_arg = None
        self.curr_instr = self.r2_obj.debug_pdj_single(pc)
        self.opcode = self.get_opcode()

    def get_opcode(self):
        return self.curr_instr[0]["opcode"]

    def is_memory_write(self):
        self.first_arg = Instruction.get_first_arg(self.get_opcode())
        is_pointer_rule = re.compile(r""".*\[(.*)\]""", re.VERBOSE)
        self.is_pointer = is_pointer_rule.match(self.first_arg)
        if self.is_pointer:
            return True
        return False

    def is_memory_read(self):
        self.second_arg = Instruction.get_second_arg(self.get_opcode())
        is_pointer_rule = re.compile(r""".*\[(.*)\]""", re.VERBOSE)
        self.is_pointer = is_pointer_rule.match(self.second_arg)
        if self.is_pointer:
            return True
        return False

    def is_branch_instr(self):
        branch_list = ["ucall", "call", "ujmp", "ucjmp"]
        if self.curr_instr[0]["type"] in branch_list:
            return True
        return False

    def write_size(self):
        types = {"byte": 1, "word": 2, "dword": 4}
        for type, value in types.items():
            if type in self.first_arg:
                return value
        return False

    def get_dest_address(self):
        if self.is_pointer:
            address = self.first_arg[self.first_arg.find("[") + 1:self.first_arg.find("]")].strip()
            dest_address = self.r2_obj.debug_expression(address)
            dest_address = dest_address.split()[1]
            return dest_address
        return False

    def call_check(self, regs):
        """If after max 7 instruction there is call reg, it could be exploitable (e.g UAF)

        :return: True if there is a call reg instruction
        """
        instrs = self.r2_obj.debug_pdj_num("7", self.curr_instr)

        #check if "call reg" is there
        for elem in instrs:
            if elem["type"] == "ucall":
                opcode = elem["opcode"].split()
                call_arg = opcode[1]
                if call_arg in regs:
                    return True
        return False

    @staticmethod
    def get_first_arg(ocpode):
        before_comma = ocpode.split(",")[0]
        return before_comma

    @staticmethod
    def get_second_arg(ocpode):
        after_comma = ocpode.split(",")[1]
        return after_comma