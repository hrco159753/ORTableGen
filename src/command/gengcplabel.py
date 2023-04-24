import json

import command.util as util

class GenGcpLabel:

    def init(self, sub_parsers):
        gengcplabels_parser = sub_parsers.add_parser('gengcplabel', help = 'Generate generic control point labels.')
        gengcplabels_parser.add_argument('-i', '--input', type = str, help = 'Input that supplies generic control points. By default it takes input from standard in. Input format is JSON.')
        gengcplabels_parser.add_argument('-o', '--output', type = str, help = 'Output to where the generic control points labels should be written. By default it writes the output to standard out. Output format is PDF.')
        gengcplabels_parser.add_argument('-cw', '--cell_width', type = int, help = 'Cell width. By default cell width is set to 150.', default = 150)
        gengcplabels_parser.add_argument('-ch', '--cell_height', type = int, help = 'Cell height. By default cell width is set to 70.', default = 70)
        gengcplabels_parser.add_argument('-fs', '--font_size', type = int, help = 'Font size. By default is set to 20.', default = 20)
        gengcplabels_parser.set_defaults(func = GenGcpLabel.run)

    def run(args):
        if args.input == None:
            gcps = json.load(sys.stdin)
        else:
            with open(args.input, 'r') as handle:
                gcps = json.load(handle)

        util.generate_generic_point_labels(filename = args.output, generic_control_points = gcps, cell_width = args.cell_width, cell_height = args.cell_height, fontsize = args.font_size)
