#!/usr/bin/python3

import generators.points as points

import argparse
import json
import xlwt

def generateTable(wb, jsonPoints):
    ws = wb.add_sheet("Points")

    ws.write(0, 0, 'Point name')
    ws.write(0, 1, 'Code')
    for i, (pointName, pointCharArray) in enumerate(jsonPoints.items()):
        ws.write(i+1, 0, pointName)
        ws.write(i+1, 1, ''.join(pointCharArray))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help = 'File to point table info.' , required = True)
    parser.add_argument('-o', '--output', help = 'File where to put point table.' , required = True)

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        jsonPoints = json.load(f)
        
    wb = xlwt.Workbook()

    generateTable(wb, jsonPoints)

    wb.save(args.output)

if __name__ == '__main__':
    main()