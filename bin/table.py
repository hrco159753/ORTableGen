#!/usr/bin/python3

import generators.points as points
import generators.teams as teams
import generators.pointAquisitionCodes as aquisition

import argparse
import json
import xlwt

def generateFillingTables(wb, genPoints):
    ws = wb.add_sheet("Filling table")

    ws.write(0, 0, 'Point name')
    ws.write(0, 1, 'Aquisition code')

    for i, (point_name, _) in enumerate(genPoints.items()):
        ws.write(i+1, 0, point_name)

def generateTable(wb, genPoints, genTeams, genAquisition):
    ws = wb.add_sheet("Generated data")

    ws.write(0, 0, 'Point name')
    ws.write(0, 1, 'Point code')
    for i, (pointName, pointArray) in enumerate(genPoints.items()):
        ws.write(i+1, 0, pointName)
        ws.write(i+1, 1, ''.join(pointArray))

    ws.write(0, 4, 'Team name')
    ws.write(0, 5, 'Team code')
    for i, (teamName, teamIndexArray) in enumerate(genTeams.items()):
        ws.write(i+1, 4, teamName)
        ws.write(i+1, 5, ''.join(map(str, teamIndexArray)))

    for i, (pointName, _) in enumerate(genPoints.items()):
        ws.write(i+1, 8, pointName)

    for i, (teamName, teamAquisitionCodePerPoint) in enumerate(genAquisition.items()):
        ws.write(0, 9+i, teamName)
        for j, (pointName, teamAquisitionCode) in enumerate(teamAquisitionCodePerPoint.items()):
            ws.write(j+1, 9+i, ''.join(teamAquisitionCode))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-mc', '--mandatory_count', help = 'Count of mandatory points.', required = True)
    parser.add_argument('-oc', '--optional_count', help = 'Count of optional points.', required = True)
    parser.add_argument('-ml', '--mandatory_letter', help = 'Letter that will be prependet to every mandatory number.')
    parser.add_argument('-ol', '--optional_letter', help = 'Letter that will be prependet to every optional number.')
    parser.add_argument('-tni', '--team_names_input', help = 'File that contains the list of team names, each on seperate line.' , required = True)
    parser.add_argument('-pcal', '--point_char_array_length', help = 'Length of the point char array.', required = True)
    parser.add_argument('-tias', '--team_index_array_size', help = 'Team index array size.', required = True)
    parser.add_argument('-o', '--output', help = 'File where to output table.' , required = True)

    args = parser.parse_args()

    points_generate_opt_parameters = {key: value for key, value in filter(lambda x: x == None, [('mandatory_letter', args.mandatory_letter), ('optional_letter', args.optional_letter)])}
    genPoints = points.generate(char_array_length = int(args.point_char_array_length), mandatory_count = int(args.mandatory_count), optional_count = int(args.optional_count), **points_generate_opt_parameters)

    teamNames = []
    with open(args.team_names_input, 'r') as f:
        teamNames.extend(map(lambda x: x.strip(), f.readlines()))
    genTeams = teams.generate(team_names = teamNames, index_array_length = int(args.team_index_array_size), max_index = int(args.point_char_array_length)-1)

    genAquisition = aquisition.generate(points = genPoints, teams = genTeams)


    wb = xlwt.Workbook()
    generateTable(wb, genPoints, genTeams, genAquisition)

    generateFillingTables(wb, genPoints)

    wb.save(args.output)

if __name__ == '__main__':
    main()