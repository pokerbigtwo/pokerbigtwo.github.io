import argparse

from pycg.pycg import CallGraphGenerator
from pycg import formats
from pycg.utils.constants import CALL_GRAPH_OP, KEY_ERR_OP

from pyllow import HookGenerator

# parse argument
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entry_point",
        nargs="*",
        help="Entry points to be processed")
    parser.add_argument(
        "--package",
        help="Package containing the code to be analyzed",
        default=None
    )
    parser.add_argument(
        "--fasten",
        help="Produce call graph using the FASTEN format",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--product",
        help="Package name",
        default=""
    )
    parser.add_argument(
        "--forge",
        help="Source the product was downloaded from",
        default=""
    )
    parser.add_argument(
        "--version",
        help="Version of the product",
        default=""
    )
    parser.add_argument(
        "--timestamp",
        help="Timestamp of the package's version",
        default=0
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        help=("Maximum number of iterations through source code. " +
            "If not specified a fix-point iteration will be performed."),
        default=-1
    )
    parser.add_argument(
        '--operation',
        type=str,
        choices=[CALL_GRAPH_OP, KEY_ERR_OP],
        help=("Operation to perform. " +
             "Choose " + CALL_GRAPH_OP + " for call graph generation (default)" +
             " or " + KEY_ERR_OP + " for key error detection on dictionaries."),
        default=CALL_GRAPH_OP
    )

    parser.add_argument(
        "--as-graph-output",
        help="Output for the assignment graph",
        default=None
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )

    # add for pyllow
    parser.add_argument(
        "-f",
        "--filename",
        help="Output hook filename",
        default="output.py"
    )

    args = parser.parse_args()
    print("Generating call graph for entry point: " + str(args.entry_point))
    cg = CallGraphGenerator(args.entry_point, args.package,
                        args.max_iter, args.operation)
    cg.analyze()
    # print (cg.output())
    class_dep=cg.output_classes()
    # class_dep = list(class_dep.keys())
    # print(class_dep)
    if args.operation == CALL_GRAPH_OP:
        if args.fasten:
            formatter = formats.Fasten(cg, args.package,
                args.product, args.forge, args.version, args.timestamp)
        else:
            formatter = formats.Simple(cg)
        output = formatter.generate()
    else:
        output = cg.output_key_errs()
    if args.package==None:
        print("Generating hook for entry point: " + str(args.entry_point) + " in file: " + args.filename )
    else:
        print("Generating hook for entry point: " + str(args.entry_point) + " in file: " + args.filename + " for package: " + args.package)
    # script function call relation
    hg = HookGenerator(args.entry_point, args.filename, args.package)
    hg.set_cg_dep(output)
    hg.set_class_dep(class_dep)
    hg.analyze()
    print("Done")
    # output of call dependency

    # as_formatter = formats.AsGraph(cg)

    # if args.output:
    #     with open(args.output, "w+") as f:
    #         f.write(json.dumps(output))
    # else:
    #     print (json.dumps(output))

    # if args.as_graph_output:
    #     with open(args.as_graph_output, "w+") as f:
    #         f.write(json.dumps(as_formatter.generate()))

if __name__ == "__main__":
    main()