import os
import subprocess
import configparser
import sys


class DBI:

    def __init__(self, target, target_options, target_file_to_run, report_file):
        """" Initialized the object's internal data.
        """
        self.target = target
        self.target_options = target_options
        self.target_file_to_run = target_file_to_run
        self.disassembly = False
        self.cbr = False
        self.disas_func = ""
        self.wrap_function = ""
        self.wrap_function_args = 0
        self.report_file = report_file
        self.drrun_path = ""
        self.client_path = ""
        self.config()

    def runInstrumentation(self):
        dynamorio_args = []
        dynamorio_args.append(self.drrun_path)
        dynamorio_args.append("-c")
        dynamorio_args.append(self.client_path)

        dynamorio_args.append("-report_file")
        dynamorio_args.append(self.report_file)

        if self.disas_func:
            dynamorio_args.append("-disas_func")
            dynamorio_args.append(self.disas_func)

        if self.disassembly and not self.disas_func:
            dynamorio_args.append("-disassembly")

        if self.wrap_function:
            dynamorio_args.append("-wrap_function")
            dynamorio_args.append(self.wrap_function)
            dynamorio_args.append("-wrap_function_args")
            dynamorio_args.append(self.wrap_function_args)

        if self.cbr:
            dynamorio_args.append("-cbr")

        dynamorio_args.append("--")
        dynamorio_args.append(self.target)

        if (self.target_options):
            dynamorio_args.append(self.target_options)

        if (self.target_file_to_run):
            dynamorio_args.append(self.target_file_to_run)

        try:
            dynamorio = subprocess.Popen(dynamorio_args, stderr=subprocess.PIPE)
            # (dynamorio_output, error_output) = dynamorio.communicate()

            dynamorio.communicate()
        except subprocess.CalledProcessError as ex:
            print("ERROR: subprocess function: %s" % ex)
            sys.exit()

        return

    def config(self):
        config = configparser.RawConfigParser()
        config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config')
        config.read(config_file)
        self.drrun_path = config.get('dynamorio', 'drrun')
        self.client_path = config.get('dynamorio', 'client')
        self.disassembly = config.getboolean('instrumentation', 'disassembly')
        self.disas_func = config.get('instrumentation', 'disas_func')
        self.wrap_function = config.get('instrumentation', 'wrap_function')
        self.wrap_function_args = config.get('instrumentation', 'wrap_function_args')
        self.cbr = config.getboolean('instrumentation', 'cbr')
        self.verbose = config.getboolean('instrumentation', 'verbose')