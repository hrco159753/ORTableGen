import csv
import json
import sys

import command.util as util

class GenGcpName:

    def init(self, sub_parsers):
        gengcpname_parser = sub_parsers.add_parser('gengcpname', help = 'Generate generic control points names.')
        gengcpname_parser.add_argument('-n', '--number_of_generic_control_points', type = int, help = 'Number of control points for which names will be generated.', required = True)
        gengcpname_parser.add_argument('-p', '--prefix', type = str, help = 'Prefix string to a name, e.g "P", which would result in "P1", "P2" and so on. By default is set to "P".', default = 'P')
        gengcpname_parser.add_argument('-o', '--output', type = str, help = 'File where to write the generated names. By default it prints them to standard out.')
        gengcpname_parser.set_defaults(func = GenGcpName.run)

    def run(args):
        if args.output == None:
            csvwriter = csv.writer(sys.stdout)
            csvwriter.writerow(util.generate_generic_point_names(number_of_points = args.number_of_generic_control_points, prefix_string = args.prefix))
        else:
            with open(args.output, 'w') as handle:
                csvwriter = csv.writer(handle)
                csvwriter.writerow(util.generate_generic_point_names(number_of_points = args.number_of_generic_control_points, prefix_string = args.prefix))

