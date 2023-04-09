#!/usr/bin/python3

import generators.points as points
import generators.teams as teams
import generators.pointAquisitionCodes as aquisition

import argparse
import json
import random

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-tni', '--team_names_input', help = 'File that contains the list of team names, each on seperate line.' , required = True)
    parser.add_argument('-tias', '--team_index_array_size', help = 'Team index array size.', required = True)
    parser.add_argument('-mi', '--max_index', help = 'Team max index in team index array.', required = True)
    parser.add_argument('-o', '--output', help = 'File where to output team tables info.' , required = True)

    args = parser.parse_args()

    with open(args.team_names_input, 'r') as f:
        teamNames = list(map(lambda x: x.strip(), f.readlines()))

    genTeams = teams.generate(team_names = teamNames, index_array_length = int(args.team_index_array_size), max_index = int(args.max_index))

    with open(args.output, 'w') as f:
        f.write(json.dumps(genTeams, indent = 4))

if __name__ == '__main__':
    main()