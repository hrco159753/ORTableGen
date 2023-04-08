#!/usr/bin/python3

import generators.points as points
import generators.teams as teams
import generators.pointAquisitionCodes as aquisition

import argparse
import json
import xlwt

def generateTable(wb, genTeams, jsonPoints):
    ws = wb.add_sheet("Team codes")

    ws.write(0, 0, 'Team name')
    ws.write(0, 1, 'Team code')

    pointsList = list(jsonPoints.items())

    for i, (point, _) in enumerate(pointsList):
        ws.write(0, 2+i, f'{point} code')

    for i, (teamName, teamIndexArray) in enumerate(genTeams.items()):
        ws.write(i+1, 0, teamName)
        ws.write(i+1, 1, ''.join(map(str, teamIndexArray)))

    for i, (team, tiArray) in enumerate(genTeams.items()):
        for j, (_, pcArray) in enumerate(pointsList):
            value = ''.join(map(lambda index: pcArray[index], tiArray))
            ws.write(1+i, 2+j, value)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-pii', '--points_info_input', help = 'File that contains points info.' , required = True)
    parser.add_argument('-tni', '--team_names_input', help = 'File that contains the list of team names, each on seperate line.' , required = True)
    parser.add_argument('-tias', '--team_index_array_size', help = 'Team index array size.', required = True)
    parser.add_argument('-o', '--output', help = 'File where to output team tables.' , required = True)

    args = parser.parse_args()

    with open(args.points_info_input, 'r') as f:
        jsonPoints = json.load(f)

    with open(args.team_names_input, 'r') as f:
        teamNames = list(map(lambda x: x.strip(), f.readlines()))

    genTeams = teams.generate(team_names = teamNames, index_array_length = int(args.team_index_array_size), max_index = len(list(jsonPoints.values())[0])-1)

    wb = xlwt.Workbook()

    generateTable(wb, genTeams, jsonPoints)

    wb.save(args.output)

if __name__ == '__main__':
    main()