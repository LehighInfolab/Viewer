import getopt
import math
import sys
import argparse
import os
import csv


"""
Util file for parsing text files easily
	
 	- file reads in a .txt file whose separator use space chars: 
 		***specifically PDB and HBondFinder files
	
 	- file may contain a header - if so, use 'header' bool variable and 'header_size' to specify size of header
  
	Usage: parse_file( [file_name] , [optional: header - default = False] , [optional: header_size - default = 1] )

		file_name = name of file to read
		header = boolean indicating if a header is present, and will remove header lines. If header is false, header_size will not be used.
		header_size = number of lines at the top of the file that header occupies.
"""

## Main function to use in this file
def parse_file(file, header=False, header_size=1):
    lines = read_file(file)
    all_lines = parse_lines(lines, header, header_size)
    return all_lines


## Alternate main function specifically for cleaning up PDB files
def parse_PDB_file(file):
    cleaned_lines = read_PDB_lines(file)
    all_lines = parse_lines(cleaned_lines, False, 0)
    return all_lines


def help():
    print("File parses .txt files of data whose separator is empty space characters.")
    print("----------------------------------------------------------------")
    print(
        "Usage: parse_file( [file_name] , [optional: header - default = False] , [optional: header_size - default = 1] )"
    )
    print("")
    print("file_name = name of file to read")
    print(
        "header = boolean indicating if a header is present, and will remove header lines. If header is false, header_size will not be used."
    )
    print("header_size = number of lines at the top of the file that header occupies.")


def read_file(file):
    try:
        f = open(file, "r")
    except:
        print("Could not read file: ", file)
    lines = f.readlines()
    f.close()
    return lines


## Utility function to get length of header for PDB files specifically
def get_PDB_header_length(file):
    f = open(file, "r")
    count = 0
    while True:
        line = f.readline()
        if not line:
            break
        if line[0:4] == "ATOM":
            return count
        count += 1
    f.close()


def read_PDB_lines(file):
    f = open(file, "r")
    cleaned_lines = []
    while True:
        line = f.readline()
        if not line:
            break
        if line[0:4] == "ATOM":
            cleaned_lines.append(line)
    f.close()
    return cleaned_lines


def parse_lines(lines, header, header_size):
    all_lines = []
    counter = 0
    if header == False:
        counter = 0
    elif header == True:
        counter = header_size

    for i in range(counter, len(lines)):
        split_line = lines[i].split(" ")
        split_line = [i for i in split_line if i]
        split_line.pop()
        all_lines.append(split_line)
    return all_lines


# Input should be a list of lists - inner list should be information of an atom for each line of the pdb...outer list is the list of all atoms.
def write_PDB(output_name, append, atoms_list):
    if append == False:
        f = open(output_name, "w")
    elif append == True:
        f = open(output_name, "a")
    for j in atoms_list:
        j[0] = j[0].ljust(6)  # atom#6s
        j[1] = j[1].rjust(5)  # aomnum#5d
        j[2] = j[2].center(4)  # atomname$#4s
        j[3] = j[3].ljust(3)  # resname#1s
        j[4] = j[4].rjust(1)  # Astring
        j[5] = j[5].rjust(4)  # resnum
        j[6] = str("%8.3f" % (float(j[6]))).rjust(8)  # x
        j[7] = str("%8.3f" % (float(j[7]))).rjust(8)  # y
        j[8] = str("%8.3f" % (float(j[8]))).rjust(8)  # z\
        # j[9] = str("%6.2f" % (float(j[9]))).rjust(6)  # occ
        # try:
        #     j[10] = str("%6.2f" % (float(j[10]))).ljust(6)  # temp
        # except Exception as error:
        #     print(error, "-- Leaving as string.")
        #     j[10] = j[10].ljust(6)  # not temp, atom single letter code

        line = "%s%s %s %s %s%s    %s%s%s\n" % (
            j[0],
            j[1],
            j[2],
            j[3],
            j[4],
            j[5],
            j[6],
            j[7],
            j[8],
            # j[9],
            # j[10],
        )

        f.write(line)
    f.close()


def split_PDB_chain(PDB_data):
    chains = {}
    for line in PDB_data:
        chain = str(line[4])
        if chain not in chains:
            chains[chain] = []
        else:
            chains[chain].append(line)
    print("All chains in PDB:", chains.keys())
    return chains


def main():
    # print(parse_file("hbondfinder_results/HBondFinder_1A4Y.txt"))
    # data = parse_file("Dataset/F_chain_only+h.pdb")
    data = parse_file(
        "Dataset/1brs_barnase_A+h.pdb",
        True,
        get_PDB_header_length("Dataset/1brs_barnase_A+h.pdb"),
    )
    print(len(data))
    data = parse_PDB_file("Dataset/1brs_barnase_A+h.pdb")
    print(len(data))
    # get_PDB_header_length("Dataset/F_chain_only+h.pdb")
    # get_PDB_header_length("Dataset/1brs_barnase_A+h.pdb")


if __name__ == "__main__":
    main()
