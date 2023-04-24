import csv
import json
import sys

import command.util as util

class GenTeam:

    def init(self, sub_parsers):
        genteam_parser = sub_parsers.add_parser('genteam', help = 'Generate teams.')
        genteam_parser.add_argument('-i', '--input', type = str, help = 'Specify a file that contains team names. By default it takes input from standard in. Format of the input is CSV.')
        genteam_parser.add_argument('-o', '--output', type = str, help = 'Specify a file where to output generated teams. By default it puts it to the standard out. Fromt of the output is JSON.')
        genteam_parser.add_argument('-tcl', '--team_code_length', type = int, help = 'Specify the team code length. By default is set to 3.', default = 3)
        genteam_parser.add_argument('-tchi', '--team_code_highest_index', type = int, help = 'Specify what is the heighest number that can be present in team code. By default is set to 6.', default = 6)    
        genteam_parser.set_defaults(func = GenTeam.run)

    def run(args):
        if args.input == None:
            csvreader = csv.reader(sys.stdin)
            team_names = (team_name.strip() for row in csvreader for team_name in row)

            team_names = util.generate_teams(team_names = team_names, team_code_length = args.team_code_length, team_code_highest_index = args.team_code_highest_index) 
        else:
            with open(args.input, 'r') as handle:
                csvreader = csv.reader(handle)
                team_names = (team_name.strip() for row in csvreader for team_name in row)

                team_names = util.generate_teams(team_names = team_names, team_code_length = args.team_code_length, team_code_highest_index = args.team_code_highest_index) 

        if args.output == None:
            sys.stdout.write(json.dumps(team_names, indent = 4))
        else:
            with open(args.output, 'w') as handle:
                handle.write(json.dumps(team_names, indent = 4))

