from r2.r2 import *
import sys


class Crash:

    def __init__(self, software, software_args=False, file_to_run=False):
        """" Initialized the object's internal data.
        Args:
            software: The software to analyze
            software_args(optional): The software arguments
            file_to_run(optional): The crafted file
        """
        self.software = software
        self.software_args = software_args
        self.file_to_run = file_to_run
        self.r2_obj = radare2()
        self.r2_dbg_obj = None
        self.r2_stand_obj = None

    def open(self):
        try:
            r2_obj = self.r2_obj.open_file(self.software)
        except Exception as ex:
            print("Open file Exception: %s" % ex)
            exit(0)

        self.r2_dbg_obj = DebugCommands(r2_obj)
        self.r2_stand_obj = Commands(r2_obj)

        try:
            if self.software_args:
                if self.file_to_run:
                    self.r2_dbg_obj.debug_reopen(self.software_args, self.file_to_run)
                else:
                    self.r2_dbg_obj.debug_reopen_single(self.software_args)
            else:
                self.r2_dbg_obj.debug_reopen_single()
        except Exception as ex:
            print("Reopen file in debug mode (doo) Exception: %s" % ex)
            sys.exit(-1)


def main():
    run_obj = Crash("/home/invictus1306/Documents/r2conf/init_test/mytests/crash_on_pc", "", "")
    run_obj.open()


if __name__ == "__main__":
    main()