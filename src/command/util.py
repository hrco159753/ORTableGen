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
    
def draw_cell(c: canvas.Canvas, *, label, coords, celldim, border = True):
    left_bottom_to_center = lambda left_bottom_coords: (left_bottom_coords[0] + celldim[0] // 2, left_bottom_coords[1] + celldim[1] // 2 - 5)

    c.rect(*coords, *celldim, stroke = border)
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

def extract_gpc_additional_data(gpx_obj):
    def decompose_waypoint(waypoint):
        name = waypoint.name
        ext = waypoint.extensions
        alias = next(filter(lambda x: x.tag.endswith('other_name'), ext)).text
        score = next(filter(lambda x: x.tag.endswith('score'), ext)).text
        return (name, alias, score)
    return [ { "name": name, "alias": alias, "score": int(score) } for (name, alias, score) in map(decompose_waypoint, gpx_obj.waypoints) ]

def generate_cps(*, gcps, gcp_additional_data):
    gcp_names = {gcp["name"] for gcp in gcps}
    data_names = {data["name"] for data in gcp_additional_data}

    if gcp_names != data_names:
        print("Warning: Set gcps not corresponding with additonal data provided points.")

    def find_additional_data_for_gcp(gcp):
        find_corresponding_data = lambda data: data["name"] == gcp["name"]
        return next(filter(find_corresponding_data, gcp_additional_data))

    gcps_with_data = ((gcp, find_additional_data_for_gcp(gcp)) for gcp in gcps)
    return [{"name": gcp["name"], "code": gcp["code"], "alias": data["alias"], "score": int(data["score"])} for (gcp, data) in gcps_with_data]

def generate_acquisition_tables(*, output_stream, cps, teams):
    c = canvas.Canvas(output_stream, pagesize = A4)

    combine_labels = ((name, alias, "") for (name, alias) in ((cp["name"], cp["alias"]) for cp in cps))
    combine_labels = [item for tuple in combine_labels for item in tuple]
    celldim = (100, 50)
    right_margin, bottom_margin = 100, -10

    for team in teams:
        c.setFontSize(20)
        draw_table(c, labels = ["Name", "Alias", "Code"] + combine_labels, tabledim = (3, 1+len(cps)), pagedim = (A4[0], A4[1] - 20))
        draw_cell(c, label = f"{team['name']}: {' '.join(team['code'])}", coords = (A4[0] - celldim[0] - right_margin, bottom_margin), celldim = celldim, border = False)
        c.showPage()
    c.save()
