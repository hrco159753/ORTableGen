import random
import string
import json
import csv
import xlsxwriter as xlsx
import itertools

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

def generate_workbook(*, output_file, cps, teams, maximum_additional_points = 0):
    workbook = xlsx.Workbook(output_file)

    point_worksheet = workbook.add_worksheet("Points")

    header_row = ("Name", "Code", "Alias", "Score")
    other_rows = ((cp["name"], cp["code"], cp["alias"], cp["score"]) for cp in cps)
    for (i, (name, code, alias, score)) in enumerate(itertools.chain([header_row], other_rows)):
        point_worksheet.write(i, 0, name)
        point_worksheet.write(i, 1, code)
        point_worksheet.write(i, 2, alias)
        point_worksheet.write(i, 3, score)

    point_worksheet.write(0, 5, "Max points from CPs")
    point_worksheet.write(1, 5, f"=SUM(D2:D{len(cps) + 1})")

    point_worksheet.write(0, 6, 'Maximum additional points')
    point_worksheet.write(1, 6, maximum_additional_points)

    point_worksheet.write(0, 7, 'Maximum points')
    point_worksheet.write(1, 7, "=SUM(E2:F2)")

    point_worksheet.autofit()


    team_worksheet = workbook.add_worksheet("Teams")
    header_row = ("Name", "Code", "Time", "CP score", "Additional score", "Total score")
    other_rows = ((team["name"], team["code"], f"='{team['name']}'!G2", f"='{team['name']}'!H2", f"='{team['name']}'!I2", f"='{team['name']}'!J2") for team in teams)

    for (i, (name, code, time, cp_score, additional_score, total_score)) in enumerate(itertools.chain([header_row], other_rows)):
        team_worksheet.write(i, 0, name)
        team_worksheet.write(i, 1, code)
        team_worksheet.write(i, 2, time)
        team_worksheet.write(i, 3, cp_score)
        team_worksheet.write(i, 4, additional_score)
        team_worksheet.write(i, 5, total_score)

    team_worksheet.write(4, 9, 'Winner')
    team_worksheet.write(5, 9, '=INDIRECT(ADDRESS(MATCH(MAX(F2:F3),F:F,1),1))')

    team_worksheet.autofit()

    for team in teams:
        team_worksheet = workbook.add_worksheet(team["name"])

        def get_acquisition_code(team_code, point_code):
            point_code = [c for c in point_code]
            return ''.join((point_code[i] for i in map(int,team_code)))

        header_row = ("Point name", "Acquisition code", "Point score", "Did acquire?", "Score")
        other_rows = (((cp["name"], get_acquisition_code(team["code"], cp["code"]), f"=Points!D{2+i}", "No", f'=IF(D{2+i}<>"No", C{2+i}, 0)')) for (i, cp) in enumerate(cps))

        for (i, (point_name, acq_code, point_score, did_acquire, score)) in enumerate(itertools.chain([header_row], other_rows)):
            team_worksheet.write(i, 0, point_name)
            team_worksheet.write(i, 1, acq_code)
            team_worksheet.write(i, 2, point_score)
            team_worksheet.write(i, 3, did_acquire)
            team_worksheet.write(i, 4, score)

        team_worksheet.write(0, 6, 'Time')
        team_worksheet.write(1, 6, "")

        team_worksheet.write(0, 7, "CP score sum")
        team_worksheet.write(1, 7, f"=SUM(E2:D{len(cps) + 1})")

        team_worksheet.write(0, 8, 'Additional points')
        team_worksheet.write(1, 8, "")

        team_worksheet.write(0, 9, 'Total points')
        team_worksheet.write(1, 9, "=SUM(H2:I2)")

        team_worksheet.autofit()

    workbook.close()