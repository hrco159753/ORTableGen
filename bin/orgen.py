#!/usr/bin/env python

import sys
import argparse
import json
import csv
import random
import string

from collections import namedtuple
from more_itertools import chunked

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_generic_points(*, point_names: list[str], point_code_length: int) -> list[dict[str, str]]:
    gencode = lambda : ''.join((random.choice(string.ascii_uppercase) for _ in range(point_code_length)))
    return [{'name': point_name, 'code': gencode()} for point_name in point_names]

def generate_teams(*, team_names: list[str], team_code_length: int, team_code_highest_index: int) -> list[dict[str, str]]:
    assert team_code_highest_index >= 0 and team_code_highest_index <=9, "Two digits index are not supported."

    gencode = lambda : ''.join(map(str, (random.randint(0, team_code_highest_index) for _ in range(team_code_length))))
    return [{'name': team_name, 'code': gencode()} for team_name in team_names]

def generate_generic_point_names(*, number_of_points: int, prefix_string: str) -> list[str]:
    return [f'{prefix_string}{i}' for i in range(1, number_of_points+1)]
    
def draw_cell(c: canvas.Canvas, *, label, coords, celldim):
    left_bottom_to_center = lambda left_bottom_coords: (left_bottom_coords[0] + celldim[0] // 2, left_bottom_coords[1] + celldim[1] // 2)

    c.rect(*coords, *celldim)
    c.drawCentredString(*left_bottom_to_center(coords), label)


def draw_table(c: canvas.Canvas, *, labels, tabledim, pagedim):
    assert len(labels) <= tabledim[0] * tabledim[1]

    celldim = (pagedim[0] // tabledim[0], pagedim[1] // tabledim[1])

    index_to_coord = lambda i: (celldim[0] * (i % tabledim[0]), A4[1] - celldim[1] * (1 + (i // tabledim[0]))) 
    cellcords = (index_to_coord(i) for i in range(0, tabledim[0] * tabledim[1]))
    for (coords, label) in zip(cellcords, labels):
        draw_cell(c, label = label, coords = coords, celldim = celldim)
    
def draw_pages(c: canvas.Canvas, *, all_labels, tabledim, pagedim):
    for chunked_labels in chunked(all_labels, tabledim[0] * tabledim[1]):
        draw_table(c, labels = list(chunked_labels), tabledim = tabledim, pagedim = pagedim)
        c.showPage()

    c.save()
    
def generate_generic_point_labels(*, filename = None, generic_control_points: list[dict[str, str]], cell_width: int, cell_height: int, fontsize: int = 20) -> None:
    tabledim = (int(A4[0] // cell_width), int(A4[1] // cell_height))
    labels = [f'{gcp["name"]}: {" ".join(c for c in gcp["code"])}' for gcp in generic_control_points]

    if filename == None:
        c = canvas.Canvas(sys.stdout, pagesize = A4)
        c.setFontSize(fontsize)
        draw_pages(c, all_labels = labels, tabledim = tabledim, pagedim = A4)
    else:
        c = canvas.Canvas(filename, pagesize = A4)
        c.setFontSize(fontsize)
        draw_pages(c, all_labels = labels, tabledim = tabledim, pagedim = A4)


def gengcp_command(args) -> None:
    if args.input == None:
        csvreader = csv.reader(sys.stdin)
        cp_names = (cp_name.strip() for row in csvreader for cp_name in row)
        control_points = generate_generic_points(point_names = cp_names, point_code_length = args.point_code_length) 
    else:
        with open(args.input, 'r') as handle:
            csvreader = csv.reader(handle)
            cp_names = (cp_name.strip() for row in csvreader for cp_name in row)
            control_points = generate_generic_points(point_names = cp_names, point_code_length = args.point_code_length) 

    if args.output == None:
        sys.stdout.write(json.dumps(control_points, indent = 4))
    else:
        with open(args.output, 'w') as handle:
            handle.write(json.dumps(control_points, indent = 4))

def genteam_command(args) -> None:
    if args.input == None:
        csvreader = csv.reader(sys.stdin)
        team_names = (team_name.strip() for row in csvreader for team_name in row)
        
        team_names = generate_teams(team_names = team_names, team_code_length = args.team_code_length, team_code_highest_index = args.team_code_highest_index) 
    else:
        with open(args.input, 'r') as handle:
            csvreader = csv.reader(handle)
            team_names = (team_name.strip() for row in csvreader for team_name in row)

            team_names = generate_teams(team_names = team_names, team_code_length = args.team_code_length, team_code_highest_index = args.team_code_highest_index) 

    if args.output == None:
        sys.stdout.write(json.dumps(team_names, indent = 4))
    else:
        with open(args.output, 'w') as handle:
            handle.write(json.dumps(team_names, indent = 4))

def gengcpname_command(args) -> None:
    if args.output == None:
        csvwriter = csv.writer(sys.stdout)
        csvwriter.writerow(generate_generic_point_names(number_of_points = args.number_of_generic_control_points, prefix_string = args.prefix))
    else:
        with open(args.output, 'w') as handle:
            csvwriter = csv.writer(handle)
            csvwriter.writerow(generate_generic_point_names(number_of_points = args.number_of_generic_control_points, prefix_string = args.prefix))

def gengcplabels_command(args) -> None:
    if args.input == None:
        gcps = json.load(sys.stdin)
    else:
        with open(args.input, 'r') as handle:
            gcps = json.load(handle)

    generate_generic_point_labels(filename = args.output, generic_control_points = gcps, cell_width = args.cell_width, cell_height = args.cell_height, fontsize = args.font_size)

def parse_arguemnts():
    parser = argparse.ArgumentParser(
        prog = 'orgen', 
        usage = './orgen <subcommand> <options>'
    )

    sub_parsers = parser.add_subparsers(required = True)

    gengcpname_parser = sub_parsers.add_parser('gengcpname', help = 'Generate generic control points names.')
    gengcpname_parser.add_argument('-n', '--number_of_generic_control_points', type = int, help = 'Number of control points for which names will be generated.', required = True)
    gengcpname_parser.add_argument('-p', '--prefix', type = str, help = 'Prefix string to a name, e.g "P", which would result in "P1", "P2" and so on. By default is set to "P".', default = 'P')
    gengcpname_parser.add_argument('-o', '--output', type = str, help = 'File where to write the generated names. By default it prints them to standard out.')
    gengcpname_parser.set_defaults(func = gengcpname_command)

    gengcp_parser = sub_parsers.add_parser('gengcp', help = 'Generate generic control points.')
    gengcp_parser.add_argument('-i', '--input', type = str, help = 'Specify a file that contains control point names. By default it takes input from standard in. Format of the input is CSV.')
    gengcp_parser.add_argument('-o', '--output', type = str, help = 'Specify a file where to output generated generic control points. By default it puts it to the standard out. Fromt of the output is JSON.')
    gengcp_parser.add_argument('-pcl', '--point_code_length', type = int, help = 'Specify the length of generic control point code. By default is set to 7.', default = 7)
    gengcp_parser.set_defaults(func = gengcp_command)

    genteam_parser = sub_parsers.add_parser('genteam', help = 'Generate teams.')
    genteam_parser.add_argument('-i', '--input', type = str, help = 'Specify a file that contains team names. By default it takes input from standard in. Format of the input is CSV.')
    genteam_parser.add_argument('-o', '--output', type = str, help = 'Specify a file where to output generated teams. By default it puts it to the standard out. Fromt of the output is JSON.')
    genteam_parser.add_argument('-tcl', '--team_code_length', type = int, help = 'Specify the team code length. By default is set to 3.', default = 3)
    genteam_parser.add_argument('-tchi', '--team_code_highest_index', type = int, help = 'Specify what is the heighest number that can be present in team code. By default is set to 6.', default = 6)    
    genteam_parser.set_defaults(func = genteam_command)

    gengcplabels_parser = sub_parsers.add_parser('gengcplabels', help = 'Generate generic control point labels.')
    gengcplabels_parser.add_argument('-i', '--input', type = str, help = 'Input that supplies generic control points. By default it takes input from standard in. Input format is JSON.')
    gengcplabels_parser.add_argument('-o', '--output', type = str, help = 'Output to where the generic control points labels should be written. By default it writes the output to standard out. Output format is PDF.')
    gengcplabels_parser.add_argument('-cw', '--cell_width', type = int, help = 'Cell width. By default cell width is set to 150.', default = 150)
    gengcplabels_parser.add_argument('-ch', '--cell_height', type = int, help = 'Cell height. By default cell width is set to 70.', default = 70)
    gengcplabels_parser.add_argument('-fs', '--font_size', type = int, help = 'Font size. By default is set to 20.', default = 20)
    gengcplabels_parser.set_defaults(func = gengcplabels_command)

    return parser.parse_args()

def main(args = None) -> None:
    if args == None:
        return
    
    args = parse_arguemnts()
    args.func(args)

if __name__ == '__main__':
    main(sys.argv)