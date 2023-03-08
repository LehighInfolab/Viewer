import getopt
import math
import sys
import argparse
import os

import PDB_HB_parser

"""
This file contains some utility functions for working with hbondfinder format
    - run hbondfinder in one function
    - make a folder for holding hbondfinder data
    - batch run hbondfinder (not yet implemented)
    - provide an input of HBondFinder file lines split using spaces, and will parse it to find intramolecular or intermolecular edges between atoms
"""


def read_and_parse_folder(dir):
    PDBlist = os.listdir(dir)
    return PDBlist


# Main function to run hbond finder on an input file. Unfortunately, no option to specify an output.
def run_hbondfinder(file):
    # make_hbondfinder_dir()
    PDBcode = file.split(".")[0]

    if os.path.getsize(file) == 0:
        return False

    print("Running hbondfinder.py ...")
    os.system(
        "python hbondfinder.py -i " + file + " -j JSON_Files/acceptors_donors_dict.json"
    )

    # if os.path.exists("/hbondfinder/HBondFinder_" + PDBcode):
    #     print("---File already ran through HBondFinder. ---")
    # else:
    #     print("Running hbondfinder.py ...")
    #     os.system(
    #         "python hbondfinder.py -i "
    #         + file
    #         + " -j JSON_Files/acceptors_donors_dict.json"
    #     )


# Util function to make a folder for collecting hbondfinder data
## NOTE: THIS FUNCTION NOT BEING USED. WRITING ALL RESULTS TO RESULTS FOLDER INSTEAD.
def make_hbondfinder_dir():
    print("Creating hbondfinder folder for collecting results...")
    try:
        os.mkdir("hbondfinder_data")
        print("---Successfully created folder---")
    except OSError as error:
        print("---Directory already exists. Adding files to existing directory---")


# Not yet tested or working
def batch_run_hbondfinder(dir):
    make_hbondfinder_dir()
    file_list = read_and_parse_folder(dir)
    for each in file_list:
        os.system(
            "python hbondfinder.py -i ./"
            + dir
            + "/"
            + each
            + " -j JSON_Files/acceptors_donors_dict.json"
        )


# Takes lines from an HBondFinder file split using spaces, as done by PDB_HB_Parser.parse_file(). Will extract donor and acceptor atoms and distances, and return hbond "edges" as a list of all [ donor, acceptor, dist ] edges.
def parse_hbond_lines(lines, intermolecular=False):
    edges = []
    for line in lines:
        if line[0] == line[4]:
            same_chain = True
        else:
            same_chain = False

        if intermolecular == False or same_chain == False:
            donor = line[0] + line[1]
            acceptor = line[4] + line[5]
            dist = line[8]
            edge = [donor, acceptor, dist]
            edges.append(edge)

    return edges


def main():
    # os.chdir(hbondfinder_path)
    lines = PDB_HB_parser.parse_file("HBondFinder_1A4Y", header=True, header_size=1)
    parse_hbond_lines(lines, inter=False)


if __name__ == "__main__":
    main()
