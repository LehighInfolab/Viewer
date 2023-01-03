import pandas as pd
import csv
import getopt
import math
import sys
import argparse
import os
import shutil


""" 
Parser for hbond file format
- File is formatted in two sections:
    1. Coordinate and information of all atoms
    2. The index of atoms that form the hbond

For atom info, each line contains the following separated by blank space:
[Chain] [Amino Acid] [Amino Acid #] [Atom element] [Not sure] [Coord x] [Coord y] [Coord z] [Not sure]

For hbond index, each line contains two numbers with the index of the atoms that form a hbond.
"""


def main(file):
    # Example file to parse
    file = open(file)

    # Read header which tells us number of atoms in the file
    header = file.readline()
    num_atoms = header.split()[1]
    print("NUM ATOMS:", num_atoms)

    # Arrays to hold our atom coord and hb index information
    atom_coords = []
    hb_atoms = []

    # Bools to indicate when we finished checking a section
    checking_atoms = True
    checking_bond = False

    # Checking atom info
    while checking_atoms:
        line = file.readline()
        if line[0] == "#":
            checking_atoms = False
            checking_bond = True
        atom_coords.append(line.split())

    # Checking hbond index info
    while checking_bond:
        line = file.readline()
        if not line:
            break
        hb_atoms.append(line.split())

    # Parsed results to be used
    print(atom_coords)
    print(hb_atoms)


if __name__ == "__main__":
    main()
