import json
import sys

import command.util as util

class GenWorkbook:

    def init(self, sub_parsers):
        genworkbook_parser = sub_parsers.add_parser('genworkbook', help = 'Generate work book.')
        genworkbook_parser.add_argument('-icp', '--input_control_points', type = str, help = 'File that contains contol points. File format is JSON.', required = True)
        genworkbook_parser.add_argument('-it', '--input_teams', type = str, help = 'File that contains teams. File format is JSON.', required = True)
        genworkbook_parser.add_argument('-o', '--output', type = str, help = 'File to which spreadsheet workbook is output. File format is XLS.', required = True)
        genworkbook_parser.add_argument('-map', '--maximum_additional_points', type = int, help = 'Number of maximal additonal points.')
        genworkbook_parser.set_defaults(func = GenWorkbook.run)

    def run(args):
        optparams = {key: value for (key, value) in filter(lambda x: x[1] != None, [("maximum_additional_points", args.maximum_additional_points)])}
        with open(args.input_control_points, "r") as cps_handle, open(args.input_teams, "r") as team_handle:
            util.generate_workbook(output_file = args.output, cps = json.load(cps_handle), teams = json.load(team_handle), **optparams)
