from crash_anal.crash_anal import *
from crash_anal.crash import Crash
from crash_anal.crash_graph import *
from argparse import ArgumentParser

import os
import sys


def check_file(file):
    if not os.path.exists(file):
        sys.exit()

def main():

    graph = False
    target_arg = None
    file = None
    graph_file = None

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='target program to analyze', required=True)
    parser.add_argument('-a', '--targetargs', dest='targetargs', help='arguments for the target program')
    parser.add_argument('-f', '--file', dest='file', help='input file')
    parser.add_argument('-g', '--graph', dest='graph', help='generate the graph')

    options = parser.parse_args()

    if not options.target:
        parser.error('target not given')
        return 0

    target = options.target
    check_file(target)

    if options.targetargs:
        target_arg =  options.targetargs

    if options.file:
        file = options.file
        check_file(file)

    if options.graph:
        graph = True
        graph_file = options.graph

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


