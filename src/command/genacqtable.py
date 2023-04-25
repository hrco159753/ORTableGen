import sys
import command.util as util
import json

class GenAcqTable:

    def init(self, subparsers):
        genacqtable_parser = subparsers.add_parser('genacqtable', help = 'Generate acquisition table.')
        genacqtable_parser.add_argument('-icp', '--input_cp', type = str, help = 'Specify a file that contains control point. Format of the input is JSON.', required = True)
        genacqtable_parser.add_argument('-it', '--input_teams', type = str, help = 'Specify a file that contains teams. Format of the input is JSON.', required = True)
        genacqtable_parser.add_argument('-o', '--output', type = str, help = 'Specify file where acquisition table be output. Format of the output is PDF.', required = True)
        genacqtable_parser.set_defaults(func = GenAcqTable.run)

    def run(args):
        with open(args.input_cp, 'r') as cps_handle, open(args.input_teams, 'r') as teams_handle:
            cps = json.load(cps_handle)
            teams = json.load(teams_handle)

        with open(args.output, "wb") as handle:
            util.generate_acquisition_tables(output_stream = handle, cps = cps, teams = teams)