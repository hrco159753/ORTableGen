import random
import string
import json
import csv

from collections import namedtuple
from more_itertools import chunked

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_generic_points(*, point_names, point_code_length: int):
    gencode = lambda : ''.join((random.choice(string.ascii_uppercase) for _ in range(point_code_length)))
    return [{'name': point_name, 'code': gencode()} for point_name in point_names]

def generate_teams(*, team_names, team_code_length: int, team_code_highest_index: int):
    assert team_code_highest_index >= 0 and team_code_highest_index <=9, "Two digits index are not supported."

    gencode = lambda : ''.join(map(str, (random.randint(0, team_code_highest_index) for _ in range(team_code_length))))
    return [{'name': team_name, 'code': gencode()} for team_name in team_names]

def generate_generic_point_names(*, number_of_points: int, prefix_string: str):
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
    
def generate_generic_point_labels(*, filename = None, generic_control_points, cell_width: int, cell_height: int, fontsize: int = 20) -> None:
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
