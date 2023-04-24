import csv
import json

import command.util as util

class GenGcp:

    def init(self, sub_parsers):
        gengcp_parser = sub_parsers.add_parser('gengcp', help = 'Generate generic control points.')
        gengcp_parser.add_argument('-i', '--input', type = str, help = 'Specify a file that contains control point names. By default it takes input from standard in. Format of the input is CSV.')
        gengcp_parser.add_argument('-o', '--output', type = str, help = 'Specify a file where to output generated generic control points. By default it puts it to the standard out. Fromt of the output is JSON.')
        gengcp_parser.add_argument('-pcl', '--point_code_length', type = int, help = 'Specify the length of generic control point code. By default is set to 7.', default = 7)
        gengcp_parser.set_defaults(func = GenGcp.run)

    def run(args):
        if args.input == None:
            csvreader = csv.reader(sys.stdin)
            cp_names = (cp_name.strip() for row in csvreader for cp_name in row)
            control_points = util.generate_generic_points(point_names = cp_names, point_code_length = args.point_code_length) 
        else:
            with open(args.input, 'r') as handle:
                csvreader = csv.reader(handle)
                cp_names = (cp_name.strip() for row in csvreader for cp_name in row)
                control_points = util.generate_generic_points(point_names = cp_names, point_code_length = args.point_code_length) 

        if args.output == None:
            sys.stdout.write(json.dumps(control_points, indent = 4))
        else:
            with open(args.output, 'w') as handle:
                handle.write(json.dumps(control_points, indent = 4))

