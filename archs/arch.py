import sys


class Arch:

    def __init__(self, r2_obj):
        """ Initialized the object's internal data """
        if r2_obj:
            self.r2_obj = r2_obj
            self.arch = self.get_arch()
            self.bits = self.get_bits()

    def get_arch(self):
        return self.r2_obj.cmd('e asm.arch')

    def get_bits(self):
        return self.r2_obj.cmd('e asm.bits')

    def get_reg(self, name):
        """ get register name for the specific Architecture
        :param: general register name
        :return: register name for the specific architecture
        """

        dict_x86_32 = {"stack_pointer": "esp", "base_pointer": "ebp", "program_counter": "eip"}
        dict_x86_64 = {"stack_pointer": "rsp", "base_pointer": "rbp", "program_counter": "rip"}

        if "x86" in self.arch and "32" in self.bits:
            for key, value in dict_x86_32.items():
                if key == name:
                    return value
        elif "x86" in self.arch and "64" in self.bits:
            for key, value in dict_x86_64.items():
                if key == name:
                    return value
        else:
            print("Architecture not supported")
            self.r2_obj.debug_quit()
            sys.exit(-1)

    def get_regs(self):
        """ get registers for the specific Architecture """

        x86_32_regs = ["eax", "ebx", "ecx", "edx", "esp", "ebp", "esi", "edi"]
        x86_64_regs = ["rax", "rbx", "rcx", "rdx", "rsp", "rbp", "rsi", "rdi"]

        if "x86" in self.arch and "32" in self.bits:
            return x86_32_regs
        elif "x86" in self.arch and "64" in self.bits:
            return x86_64_regs
        else:
            print("Architecture not supported")
            self.r2_obj.debug_quit()
            sys.exit()