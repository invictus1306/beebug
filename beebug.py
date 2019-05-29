from crash_anal.crash_anal import *
from crash_anal.crash import Crash
from crash_anal.crash_graph import *
from argparse import ArgumentParser

from instrumentation.dbi import DBI
from instrumentation.parse import Parse

import os
import sys
import datetime

def check_file(file):
    if not os.path.exists(file):
        sys.exit()

def main():

    graph = False
    target_arg = ""
    file = ""
    graph_file = ""
    instrumentation = False
    crash_anal = False
    crash_desc = ""

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', required=True, help='target program to analyze')
    parser.add_argument('-ta', '--targetargs', dest='targetargs', help='arguments for the target program')
    parser.add_argument('-f', '--file', dest='file', help='input file')
    parser.add_argument('-g', '--graph', dest='graph', help='output graph name')
    parser.add_argument('-i', '--instrumentation', dest='instrumentation', action="store_true", help='instrumentation option')
    parser.add_argument('-a', '--analyze', dest='crash_anal', action="store_true", help='analyze crash')
    parser.add_argument('-r', '--report_file', dest='report_file', help='DynamoRIO report file to parse')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.3 - 01/06/2019')

    options = parser.parse_args()

    target = options.target
    check_file(target)

    if options.targetargs:
        target_arg = options.targetargs

    if options.file:
        file = options.file
        check_file(file)

    if options.graph:
        graph = True
        graph_file = options.graph

    if options.instrumentation:
        instrumentation = True

    if options.crash_anal:
        crash_anal = True

    if crash_anal == False and instrumentation == False:
        parser.error("you must select to analyze the crash by using r2 (-a) and/or by using instrumentation (-i)")
        return

    if crash_anal:
        crash_obj = Crash(target, target_arg, file)
        crash_obj.open()

        crash_obj_anal = CrashAnal(crash_obj)
        crash_desc = crash_obj_anal.check_crash()

    if instrumentation:
        if options.report_file:
            report_file = options.report_file
        else:
            print("report file is required, please enter it!")
            sys.exit()

        if graph:
            out_pdf_file = graph_file
        else:
            unique_filename = "out_pdf_file" + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
            out_pdf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), unique_filename)

        instrumentation_obj = DBI(target, target_arg, file, report_file)
        instrumentation_obj.runInstrumentation()

        instrumentation_graph_obj = Parse(report_file, out_pdf_file, crash_desc)
        instrumentation_graph_obj.read_file()

if __name__ == "__main__":
    main()