"""
Authors: Killian Nucci, Damien Touati
"""

from board import Board
import argparse
from board_loader import *
import sys


def main():
    sys.setrecursionlimit(10000)
    parser = argparse.ArgumentParser(
        description='Map  choise'
    )
    parser.add_argument(
        '--file',
        '-f',
        type=str,
        default="square/map3.txt",
        help="File name"
    )
    parser.add_argument(
        '--theme',
        '-t',
        type=str,
        default="classique",
        help="collection theme"
    )
    args = parser.parse_args()
    loader = BoardLoader(args.file)
    board = Board(loader.pawns, loader.sheeps,loader.width, loader.height, args.theme)
    board.play()


if __name__ == "__main__":
    main()