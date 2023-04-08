#!/usr/bin/python3

import argparse
import json
import xlwt

def generateFillingTables(wb, jsonPoints):
    ws = wb.add_sheet("Filling table")

    ws.write(0, 0, 'Point name')
    ws.write(0, 1, 'Code')

    for i, (point_name, _) in enumerate(jsonPoints.items()):
        ws.write(i+1, 0, point_name)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help = 'Json file from which points are read.', required = True)
    parser.add_argument('-o', '--output', help = 'File where to output table.' , required = True)

    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        jsonPoints = json.load(f)
        
    wb = xlwt.Workbook()

    generateFillingTables(wb, jsonPoints)

    wb.save(args.output)

if __name__ == '__main__':
    main()