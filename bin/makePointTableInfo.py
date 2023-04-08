#!/usr/bin/python3

import generators.points as points

import argparse
import json

def generateTable(genPoints, file_name):
    with open(file_name, 'w') as f:
        f.write(json.dumps(genPoints, indent = 4))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-mc', '--mandatory_count', help = 'Count of mandatory points.', required = True)
    parser.add_argument('-oc', '--optional_count', help = 'Count of optional points.', required = True)
    parser.add_argument('-pcal', '--point_char_array_length', help = 'Number of characters in point array.', required = True)
    parser.add_argument('-o', '--output', help = 'File where to point table info.' , required = True)

    args = parser.parse_args()

    genPoints = points.generate(char_array_length = int(args.point_char_array_length), mandatory_count = int(args.mandatory_count), optional_count = int(args.optional_count))

    generateTable(genPoints, args.output)

if __name__ == '__main__':
    main()