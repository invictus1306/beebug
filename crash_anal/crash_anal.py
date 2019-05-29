from crash_anal.engine import Engine
from crash_anal.checks import Checks


class CrashAnal:

    def __init__(self, object):
        """" Initialized the object's internal data.
        Args:
            object: Crash object
        """
        self.r2_obj = object.r2_obj
        self.r2_dbg_obj = object.r2_dbg_obj
        self.r2_stand_obj = object.r2_stand_obj
        self.get_info = None

    def check_crash(self):

        self.r2_stand_obj.analyze()
        self.r2_dbg_obj.debug_continue()
        self.r2_dbg_obj.debug_dmmSy()
        self.r2_dbg_obj.debug_setenv("dbg.btdepth", "256")

        self.get_info = self.r2_dbg_obj.debug_infoj()
        signal = self.get_info["signal"]

        is_expoitable = CrashAnal.exploitable(signal, self.r2_dbg_obj)

        self.r2_dbg_obj.debug_quit()

        return is_expoitable

    @staticmethod
    def exploitable(signal, r2_dbg_obj):

        if not Checks.check_signal(signal):
            print("Signal type %s is an Uncategorized Signal" % signal)
            return False

        engine = Engine(r2_dbg_obj)

        #check access violation signal
        if Checks.check_signal(signal):

            ret_exploitable = engine.stack_overf_libc()
            if ret_exploitable:
                return ret_exploitable

            ret_exploitable = engine.crash_on_pc()
            if ret_exploitable:
                return ret_exploitable

            ret_exploitable = engine.crash_on_branch()
            if ret_exploitable:
                return ret_exploitable

            ret_exploitable = engine.invalid_write()
            if ret_exploitable:
                return ret_exploitable

            ret_exploitable = engine.heap_error()
            if ret_exploitable:
                return ret_exploitable

            ret_exploitable = engine.read_access_violation()
            if ret_exploitable:
                return ret_exploitable

        engine.not_exploitable()
        return False