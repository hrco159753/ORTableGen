import sys
import command.util as util
import gpxpy
import json

class GenCp:

    def init(self, subparsers):
        gencp_parser = subparsers.add_parser('gencp', help = 'Generate control points.')
        gencp_parser.add_argument('-igcp', '--input_gcp', type = str, help = 'Specify a file that contains generic control point. Format of the input is JSON.', required = True)
        gencp_parser.add_argument('-igcpa', '--input_gcp_additional', type = str, help = 'Specify a file that contains additional data to generic control point. Format of the input is GPX.', required = True)
        gencp_parser.add_argument('-o', '--output', type = str, help = 'Specify file where control points will be output. By defualt it sends them to standard output. Format of the output is JSON.')
        gencp_parser.set_defaults(func = GenCp.run)

    def run(args):
        with open(args.input_gcp, 'r') as gcps_handle, open(args.input_gcp_additional, 'r') as gpx_data_handle:
            gcp_additional_data = util.extract_gpc_additional_data(gpxpy.parse(gpx_data_handle))
            cps = util.generate_cps(gcps = json.load(gcps_handle), gcp_additional_data = gcp_additional_data)

        if args.output == None:
            sys.stdout.write(json.dumps(cps, indent = 4))
        else:
            with open(args.output, "w") as handle:
                handle.write(json.dumps(cps, indent= 4))