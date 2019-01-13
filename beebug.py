from crash_anal.crash_anal import *
from crash_anal.crash import Crash
from crash_anal.crash_graph import *
from argparse import ArgumentParser
from instrumentation.parse import Parse

import os
import sys
import datetime

def check_file(file):
    if not os.path.exists(file):
        sys.exit()

def main():

    graph = False
    target_arg = None
    file = None
    graph_file = None
    instrumentation = False

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='target program to analyze')
    parser.add_argument('-a', '--targetargs', dest='targetargs', help='arguments for the target program')
    parser.add_argument('-f', '--file', dest='file', help='input file')
    parser.add_argument('-g', '--graph', dest='graph', help='generate the graph')
    parser.add_argument('-i', '--instrumentation', dest='instrumentation',action="store_true", help='instrumentation option')
    parser.add_argument('-r', '--report_file', dest='report_file', help='DynamoRIO report file to parse')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.2 - 13/01/2019')

    options = parser.parse_args()

    if options.target:
        target = options.target
        check_file(target)
    elif options.instrumentation:
        instrumentation = True
    else:
        parser.error('target not given and instrumentation option not used!')
        return 0

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

    if instrumentation:
        if options.report_file:
            report_file = options.report_file
        else:
            print("report file is required, please enter it!")
            sys.exit()

        if graph:
            out_png_file = graph_file
        else:
            unique_filename = "out_png_file" + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
            out_png_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), unique_filename)

        instrumentation_graph_obj = Parse(report_file, out_png_file)
        instrumentation_graph_obj.read_file()
        return

    crash_obj = Crash(target, target_arg, file)
    crash_obj.open()

    if graph:
        crash_graph = CrashGraph(crash_obj, graph_file)
        crash_graph.crash_graph()
    else:
        crash_anal = CrashAnal(crash_obj)
        crash_anal.check_crash()

if __name__ == "__main__":
    main()


