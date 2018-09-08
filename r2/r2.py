import r2pipe


class radare2:

    def __init__(self):
        self.r2_obj = None

    def open_file(self, filename):
            self.r2_obj = r2pipe.open(filename)
            return self.r2_obj

    def cmd(self, command):
        return self.r2_obj.cmd(command)

    def cmdj(self, command):
        return self.r2_obj.cmdj(command)

    def debug_quit(self):
        return self.r2_obj.quit()


class DebugCommands(radare2):

    def __init__(self, r2_obj):
        self.r2_obj = r2_obj

    def debug_continue(self):
        return super(DebugCommands, self).cmd("dc")

    def debug_break(self, address):
        return super(DebugCommands, self).cmd('db ' + address)

    def debug_dbu(self, address):
        return super(DebugCommands, self).cmd('dbu ' + address)

    def debug_registers(self):
        return super(DebugCommands, self).cmd("dr")

    def debug_register(self, register):
        return super(DebugCommands, self).cmd("dr " + register)

    def debug_reopen(self, software_args, file_to_run):
        return super(DebugCommands, self).cmd('doo' + software_args + ' ' + file_to_run)

    def debug_reopen_single(self, software_args=False):
        if software_args:
            return super(DebugCommands, self).cmd('doo' + software_args)
        else:
            return super(DebugCommands, self).cmd('doo')

    def debug_infoj(self):
        return super(DebugCommands, self).cmdj("dij")

    def debug_dbt(self):
        return super(DebugCommands, self).cmd("dbt")

    def debug_dmmSy(self):
        return super(DebugCommands, self).cmd(".dmm*")

    def debug_pdj_num(self, num, address):
        return super(DebugCommands, self).cmdj("pdj " + num )

    def debug_pdj_single(self, address):
        return super(DebugCommands, self).cmdj("pdj 1 @ " + address)

    def debug_setenv(self, variable_name, value):
        return super(DebugCommands, self).cmd("e " + variable_name + " = " + value)

    def debug_px(self, bytes, address):
        return super(DebugCommands, self).cmd("px " + bytes + " @ " + address)

    def debug_expression(self, address):
        return super(DebugCommands, self).cmd("? " + address)

    def debug_quit(self):
        return super(DebugCommands, self).debug_quit()


class Commands(radare2):

    def __init__(self, r2_obj):
        self.r2_obj = r2_obj

    def analyze(self):
        return super(Commands, self).cmd("aa")

    def afl(self):
        return super(Commands, self).cmd("afl")

    def aflc(self):
        return super(Commands, self).cmd("aflc")

    def aflqj(self):
        return super(Commands, self).cmdj("aflqj")

    def infoj(self):
        return super(Commands, self).cmd("ij")