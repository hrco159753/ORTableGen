#!/usr/bin/env python

import sys
import argparse

from command.gengcp import GenGcp
from command.gengcpname import GenGcpName
from command.genteam import GenTeam
from command.gengcplabel import GenGcpLabel
from command.gencp import GenCp
from command.genacqtable import GenAcqTable
from command.genworkbook import GenWorkbook

def parse_arguemnts():
    parser = argparse.ArgumentParser(
        prog = 'orgen', 
        usage = './orgen <subcommand> <options>'
    )

    sub_parsers = parser.add_subparsers(required = True)
    commands = [GenGcp(), GenGcpName(), GenTeam(), GenGcpLabel(), GenCp(), GenAcqTable(), GenWorkbook()]

    for command in commands:
        command.init(sub_parsers)

    return parser.parse_args()

def main(args = None) -> None:
    if args == None:
        return
    
    args = parse_arguemnts()
    args.func(args)

if __name__ == '__main__':
    main(sys.argv)