import getopt
import os
import math
import sys
import argparse
import shutil
import itertools

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

import PDBGreedySearch
import PDB_HB_parser
import hbondfinder_utils

"""
DiffBond
    - This file contains code for most of the main search functions for finding atoms that meet criteria to form ionic bonds, hydrogen bonds, and salt bridges within a PDB structure.
    
    Usage: -i [ Input files ] -m [ Search Mode ] -d [ Distance threshold ] -o [ Output file name]
    
    -i          Can take 1 or 2 input files. If 1 input provided file, DiffBond will split PDB into chains and find inter-chain bonds. If 2 input provided, DiffBond will find intermolecular bonds between the two input files.
    -m        Search mode. Can be multiple combinations of the following options: Contact = c, Ionic bond = i, Hydrogen bond = h, Salt bridge = S, Cation pi = p. Must include at least 1 option.
    -d         Distance threshold for search distances between atoms, in angstrom units. 
    -o         Output file name.
"""


# Parse arguments from command line
def parseArg():
    parser = argparse.ArgumentParser(
        description="Identify all points between protein structures or chains that are within a certain distance of each other."
    )
    parser.add_argument(
        "-i",
        nargs="+",
        metavar="InputPDB",
        help="Input PDB file to be compared. If only 1 file as input, then DiffBond will find bonds between all protein chains. If 2 files as input, then DiffBond will find bonds between the 2 PDB files.",
    )
    parser.add_argument("-o", nargs="?", metavar="OutputPDB", help="Output file name")

    parser.add_argument(
        "-m",
        nargs="+",
        metavar="mode",
        help="Search mode can be multiple combinations of the following options. Must include at least 1 option. Contact = c, Ionic bond = i, Hydrogen bond = h, Salt bridge = S, Cation pi = p",
    )
    parser.add_argument(
        "-d",
        nargs="?",
        metavar="distance",
        type=float,
        help="Resolution for distance checking.",
    )

    # parse list of args
    args = parser.parse_args()
    args = vars(args)
    i_list = args["i"]
    m_list = args["m"]
    d = args["d"]
    o = args["o"]
    return i_list, m_list, d, o


# Checks a connected graph from all atoms in point1 to point2, where both point1 and point2 are lists of parsed values from a PDB file.
# If within dist, then append points1, points2, and dist as a list to output. This function uses the 3D distance equation to calculate distance.
def compareDist(points1, points2, dist):
    output = []
    for i in points1:
        for j in points2:
            d1 = (float(i[6]) - float(j[6])) ** 2
            d2 = (float(i[7]) - float(j[7])) ** 2
            d3 = (float(i[8]) - float(j[8])) ** 2
            d = math.sqrt(d1 + d2 + d3)
            if d < dist:
                edge = [i, j, d]
                output.append(edge)
    return output


# Function for finding atoms meeting ionic bond criteria. Checks a connected graph from charged atoms in point1 to point2.
# If within dist, then append points1, points2, and dist as a list to output. This function uses the 3D distance equation to calculate distance.
def compareDistIonic(points1, points2, dist):
    output = []

    # Swap lists of points1 and points2 if points1 is larger. Slight improvement in efficiency if points1 much larger since function checks point1 charge before going into 2nd for loop.
    if len(points1) > len(points2):
        temp = points1
        points1 = points2
        points2 = temp

    # Temp points lists to hold all points that meet charge criteria before calculating distance.
    p1 = []
    p2 = []
    for i in points1:
        res1 = i[3]
        atom1 = i[2]
        charge1 = get_charge_from_res(res1, atom1)
        if charge1 != 0:

            for j in points2:
                res2 = j[3]
                atom2 = j[2]
                charge2 = get_charge_from_res(res2, atom2)
                if charge2 != 0:

                    # If charge1 and charge2 are not 0, then they must be 1 or -1. If charge1 + charge2 = 0, then one must be -1 and other must be +1.
                    total_charge = charge1 + charge2
                    if total_charge == 0:
                        if i not in p1:
                            p1.append(i)
                        if j not in p2:
                            p2.append(j)

    output = compareDist(p1, p2, dist)
    return output


## Util function to check the charge of a point based on the residue and atom. This is used for getting ionic bonds.
def get_charge_from_res(res, atom):
    charge = 0
    if res == "HIS" or res == "ARG" or res == "LYS":
        if "NZ" in atom or "NE" in atom or "ND" in atom or "NH" in atom:
            charge = 1
    elif res == "ASP" or res == "GLU":
        if "OD" in atom or "OE" in atom:
            charge = -1
    return charge


# This function performs all of the pre-processing for the PDB files, and running hbondfinder on the processed structures.
def HB_processing(i_list, edges):
    atoms1 = []
    atoms2 = []
    for edge in edges:
        atoms1.append(edge[0])
        atoms2.append(edge[1])
    PDB_HB_parser.write_PDB("temp.pdb", False, atoms1)
    PDB_HB_parser.write_PDB("temp.pdb", True, atoms2)

    ### This function runs hbondfinder - function imported from hbondfinder_utils.
    ### If function returns false, that means file is empty.
    if hbondfinder_utils.run_hbondfinder("temp.pdb") == False:
        os.remove("temp.pdb")
        return

    try:
        hb_file_name = (
            i_list[0].split(".")[-2].split("\\")[-1]
            + i_list[1].split(".")[-2].split("\\")[-1]
            + ".txt"
        )
    except IndexError as error:
        print(
            "ERROR: Failed to process hydrogen bonds. Likely no hydrogens added to PDB."
        )
        return
    print(
        "RUNNING: Writing HBonds in hbondfinder_data folder to: ", hb_file_name, "..."
    )

    # If hbondfinder folder already contains a file with the same name, shutil.move will be unable to move the file and will not save your most recent run. Delete files and run again.
    try:
        shutil.copyfile("HBondFinder_temp.txt", "HBondFinder" + hb_file_name)
        # os.rename("HBondFinder_temp.txt", "HBondFinder" + hb_file_name)
        shutil.move("HBondFinder" + hb_file_name, "hbondfinder_data")
    except OSError as error:
        print(
            "ERROR: Was not able to move HBondFinder file to hbond_data folder. Check to see that HBondFinder file does not already exist."
        )
        os.remove("HBondFinder" + hb_file_name)

    try:
        shutil.copyfile("hbonds_temp.txt", "hbonds" + hb_file_name)
        # os.rename("hbonds_temp.txt", "hbonds" + hb_file_name)
        shutil.move("hbonds" + hb_file_name, "hbondfinder_data")
    except OSError as error:
        print(
            "ERROR: Was not able to move hbond file to hbond_data folder. Check to see that hbond file does not already exist."
        )
        os.remove("hbonds" + hb_file_name)

    os.remove("temp.pdb")

    try:
        print("RUNNING: Clearing temp files... ")
        os.remove("HBondFinder_temp.txt")
        os.remove("hbonds_temp.txt")
    except OSError as error:
        print("ERROR: Unable to find files to clear")

    return "HBondFinder" + hb_file_name


def interchain_HB_processing(file):
    try:
        shutil.copyfile(file, "./temp.pdb")
    except OSError as error:
        print("ERROR: Was not able to find " + file)
        return
    if hbondfinder_utils.run_hbondfinder("temp.pdb") == False:
        os.remove("temp.pdb")
        return

    hb_file_name = file.split(".")[-2].split("\\")[-1] + ".txt"
    print(
        "RUNNING: Writing HBonds in hbondfinder_data folder to: ", hb_file_name, "..."
    )

    # If hbondfinder folder already contains a file with the same name, shutil.move will be unable to move the file and will not save your most recent run. Delete files and run again.
    try:
        os.rename("HBondFinder_temp.txt", "HBondFinder" + hb_file_name)
        shutil.move("HBondFinder" + hb_file_name, "hbondfinder_data")
    except OSError as error:
        print(
            "ERROR: Was not able to move HBondFinder file to hbond_data folder. Check to see that HBondFinder file does not already exist."
        )
        os.remove("HBondFinder" + hb_file_name)

    try:
        os.rename("hbonds_temp.txt", "hbonds" + hb_file_name)
        shutil.move("hbonds" + hb_file_name, "hbondfinder_data")
    except OSError as error:
        print(
            "ERROR: Was not able to move hbond file to hbond_data folder. Check to see that hbond file does not already exist."
        )
        os.remove("hbonds" + hb_file_name)

    os.remove("temp.pdb")

    return "HBondFinder" + hb_file_name


# Util function for Removing duplicates and also parses out any atoms with # = -1 or 0
# Since changing the code to use only line indexes, duplicates will not occur so this function is unused.
def removeDupe(output):
    output = list(dict.fromkeys(output))
    for i in output:
        if i == -1:
            output.remove(-1)
        if i == 0:
            output.remove(0)
    return output


# Util function to create a directory for the current protein results
def make_results_dir(outputFileName):
    print("RUNNING: Creating folder for collecting bond results...")
    try:
        os.mkdir("Results/" + outputFileName)
        print("--- Successfully created folder ---")
    except OSError as error:
        print("ERROR: Directory already exists. Adding files to existing directory")
    results_dir = "Results/" + outputFileName
    return results_dir


# Util function for making a networkx graph object from a list of edges. Automatically puts into bipartite format.
def make_graph(edges):
    G = nx.Graph()
    pos = []
    ## make sure all nodes on left side are from the same chain
    if not edges:
        return G, pos
    left_chain = edges[0][0][0]
    left_nodes = []
    # right = []

    for edge in edges:
        ## if the first node, edge[0], is not on the same chain as left_chain, then add the other node.
        if edge[0][0] == left_chain:
            left_nodes.append(edge[0])
        else:
            left_nodes.append(edge[1])

        G.add_edge(edge[0], edge[1], weight=edge[2])
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    ## draw position of nodes on one side of interface separate from other side
    pos = nx.drawing.layout.bipartite_layout(G, left_nodes)

    return G, pos


# Util function for visualizing graph
def visualize_graph(graph, pos):
    ## set up drawing of graphs
    plt.subplot(121)
    nx.draw(graph, with_labels=True, pos=pos)
    plt.show()


# Util function just for reformatting edge format outputted by ionic bond and salt bridge edges so that they contain only [chain letter + AA number of donors, chain letter + AA number of acceptors, distance]
def reformat_contact_ionic_for_graph(edges):
    new_edges = []
    for edge in edges:
        reformat_edge = [edge[0][4] + edge[0][5], edge[1][4] + edge[1][5], edge[2]]
        if reformat_edge not in new_edges:
            new_edges.append(reformat_edge)
    return new_edges


def main():
    i_list, mode, dist, outputFileName = parseArg()
    # i_list = ["Dataset/1brs_barnase_A+h.pdb", "Dataset/1brs_barstar_D+h.pdb"]
    # mode = ["i", "h"]
    # dist = 4
    # outputFileName = None

    if dist == None:
        dist = 5.0
    else:
        dist = float(dist)

    # Set output file name if no name was given in args
    if outputFileName == None:
        outputFileName = "Result"
        for i in i_list:
            temp = str(i.split("\\")[-1])
            outputFileName = outputFileName + "_" + str(temp.split(".")[-2])
        outputFileName = outputFileName + "_" + str(dist) + "A"

    use_visual = True

    # Different process for one input file given vs 2 input files given.
    if len(i_list) == 1:
        PDB_data = PDB_HB_parser.parse_PDB_file(i)
        chains_data = PDB_HB_parser.split_PDB_chain(PDB_data)
        chains_comb = list(itertools.combinations(list(chains_data.keys()), 2))
        print(chains_comb)

        # Create folder for results to be stored. If folder already exists, then skip.
        print(
            '--- Results will be printed to "',
            outputFileName,
            '" in Results folder ---',
        )
        results_dir = make_results_dir(outputFileName)

        for c in chains_comb:
            print("RUNNING: Working on the following combination of chains", c)
            PDB_data = []
            PDB_data.append(chains_data[c[0]])
            PDB_data.append(chains_data[c[1]])

            # "Cache" the edges if they have been calculated if a mode requires multiple different bonds to calculate eg. salt bridges, graphs
            contact_edges = []
            ionic_edges = []
            hbond_edges = []

            # Switch statement for all bond functions
            for m in mode:
                if m == "c":
                    print("##### Searching contacts within " + str(dist) + "... #####")
                    contact_edges = compareDist(PDB_data[0], PDB_data[1], dist)
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print("---CONTACT DISTANCE WITHIN " + str(dist) + " DISTANCE---")
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print(contact_edges)
                elif m == "i":
                    print("##### Searching ionic bonds... #####")
                    ionic_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print(
                        "---IONIC BOND PREDICTIONS WITHIN " + str(dist) + " DISTANCE---"
                    )
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print(ionic_edges)
                elif m == "h":
                    print("##### Searching h-bonds... #####")
                    edges_temp = compareDist(PDB_data[0], PDB_data[1], 3.5)
                    hb_file = HB_processing(i_list, edges_temp)
                    if hb_file == None:
                        print("ERROR: No bonds in contact distance to run hbondfinder.")
                        break
                    hb_lines = PDB_HB_parser.parse_file(
                        "hbondfinder_data/" + hb_file, True, 1
                    )
                    hbond_edges = hbondfinder_utils.parse_hbond_lines(hb_lines, True)
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print("---H-BOND PREDICTIONS THAT MEET HBONDFINDER CRITERIA---")
                    print(
                        "--------------------------------------------------------------------------------------"
                    )
                    print(hbond_edges)

            # For modes requiring multiple bonds calculated previously (eg. salt bridges, graphs), this switch statement calculates those
            for m in mode:
                if m == "g":
                    if contact_edges == []:
                        print(
                            "##### Searching contacts within " + str(dist) + "... #####"
                        )

                        ## searching within distance for contacts
                        contact_edges = compareDist(PDB_data[0], PDB_data[1], dist)
                        reformatted_edges = reformat_contact_ionic_for_graph(
                            contact_edges
                        )

                        ## making and visualizing graph
                        contact_graph, pos = make_graph(reformatted_edges)
                        if use_visual:
                            visualize_graph(contact_graph, pos)

                        ## writing graph to file
                        nx.write_multiline_adjlist(
                            contact_graph,
                            results_dir
                            + "/contacts"
                            + "_"
                            + c[0]
                            + "_"
                            + c[1]
                            + ".adjlist",
                        )
                    if ionic_edges == []:
                        print("##### Searching ionic bonds... #####")

                        ## searching within distance for ionic bonds
                        ionic_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
                        reformatted_edges = reformat_contact_ionic_for_graph(
                            ionic_edges
                        )
                        print(reformatted_edges)

                        ## making and visualizing graph
                        ionic_graph, pos = make_graph(reformatted_edges)
                        if use_visual:
                            visualize_graph(ionic_graph, pos)

                        ## writing graph to file
                        nx.write_multiline_adjlist(
                            ionic_graph,
                            results_dir
                            + "/ionic_bonds"
                            + "_"
                            + c[0]
                            + "_"
                            + c[1]
                            + ".adjlist",
                        )

                    if hbond_edges == []:
                        print("##### Searching h-bonds... #####")

                        ## searching within distance for hbonds
                        edges_temp = compareDist(PDB_data[0], PDB_data[1], 3.5)
                        hb_file = HB_processing(i_list, edges_temp)
                        if hb_file == None:
                            print(
                                "ERROR: No bonds in contact distance to run hbondfinder."
                            )
                            break
                        hb_lines = PDB_HB_parser.parse_file(
                            "hbondfinder_data/" + hb_file, True, 1
                        )
                        hbond_edges = hbondfinder_utils.parse_hbond_lines(
                            hb_lines, True
                        )

                        ## making and visualizing graph
                        hbond_graph, pos = make_graph(hbond_edges)
                        if use_visual:
                            visualize_graph(hbond_graph, pos)

                        ## writing graph to file
                        nx.write_multiline_adjlist(
                            hbond_graph,
                            results_dir
                            + "/hbonds"
                            + "_"
                            + c[0]
                            + "_"
                            + c[1]
                            + ".adjlist",
                        )
    elif len(i_list) == 2:
        PDB_data = []
        for i in i_list:
            data = PDB_HB_parser.parse_PDB_file(i)
            PDB_data.append(data)

        # "Cache" the edges if they have been calculated if a mode requires multiple different bonds to calculate eg. salt bridges, graphs
        contact_edges = []
        ionic_edges = []
        hbond_edges = []

        # Create folder for results to be stored. If folder already exists, then skip.
        print(
            '--- Results will be printed to "',
            outputFileName,
            '" in Results folder ---',
        )
        results_dir = make_results_dir(outputFileName)

        # Switch statement for all bond functions
        for m in mode:
            if m == "c":
                print("##### Searching contacts within " + str(dist) + "... #####")
                contact_edges = compareDist(PDB_data[0], PDB_data[1], dist)
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print("---CONTACT DISTANCE WITHIN " + str(dist) + " DISTANCE---")
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print(contact_edges)
            elif m == "i":
                print("##### Searching ionic bonds... #####")
                ionic_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print("---IONIC BOND PREDICTIONS WITHIN " + str(dist) + " DISTANCE---")
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print(ionic_edges)
            elif m == "h":
                print("##### Searching h-bonds... #####")
                edges_temp = compareDist(PDB_data[0], PDB_data[1], 3.5)
                hb_file = HB_processing(i_list, edges_temp)
                if hb_file == None:
                    print("ERROR: No bonds in contact distance to run hbondfinder.")
                    break
                hb_lines = PDB_HB_parser.parse_file(
                    "hbondfinder_data/" + hb_file, True, 1
                )
                hbond_edges = hbondfinder_utils.parse_hbond_lines(hb_lines, True)
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print("---H-BOND PREDICTIONS THAT MEET HBONDFINDER CRITERIA---")
                print(
                    "--------------------------------------------------------------------------------------"
                )
                print(hbond_edges)

        # For modes requiring multiple bonds calculated previously (eg. salt bridges, graphs), this switch statement calculates those
        for m in mode:
            if m == "g":
                if contact_edges == []:
                    print("##### Searching contacts within " + str(dist) + "... #####")

                    ## searching within distance for contacts
                    contact_edges = compareDist(PDB_data[0], PDB_data[1], dist)
                    reformatted_edges = reformat_contact_ionic_for_graph(contact_edges)

                    ## making and visualizing graph
                    contact_graph, pos = make_graph(reformatted_edges)
                    if use_visual:
                        visualize_graph(contact_graph, pos)

                    ## writing graph to file
                    nx.write_multiline_adjlist(
                        contact_graph, results_dir + "/contacts.adjlist"
                    )
                if ionic_edges == []:
                    print("##### Searching ionic bonds... #####")

                    ## searching within distance for ionic bonds
                    ionic_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
                    reformatted_edges = reformat_contact_ionic_for_graph(ionic_edges)
                    print(reformatted_edges)

                    ## making and visualizing graph
                    ionic_graph, pos = make_graph(reformatted_edges)
                    if use_visual:
                        visualize_graph(ionic_graph, pos)

                    ## writing graph to file
                    nx.write_multiline_adjlist(
                        ionic_graph, results_dir + "/ionic_bonds.adjlist"
                    )

                if hbond_edges == []:
                    print("##### Searching h-bonds... #####")

                    ## searching within distance for hbonds
                    edges_temp = compareDist(PDB_data[0], PDB_data[1], 3.5)
                    hb_file = HB_processing(i_list, edges_temp)
                    if hb_file == None:
                        print("---No bonds in contact distance to run hbondfinder.---")
                        break
                    hb_lines = PDB_HB_parser.parse_file(
                        "hbondfinder_data/" + hb_file, True, 1
                    )
                    hbond_edges = hbondfinder_utils.parse_hbond_lines(hb_lines, True)

                    ## making and visualizing graph
                    hbond_graph, pos = make_graph(hbond_edges)
                    if use_visual:
                        visualize_graph(hbond_graph, pos)

                    ## writing graph to file
                    nx.write_multiline_adjlist(
                        hbond_graph, results_dir + "/hbonds.adjlist"
                    )


if __name__ == "__main__":
    main()


# TODO: still exploring whether cation pi calculations are possible.
# def compareDistCatPi(output, points1, points2, dist, splitLines_PDB1, splitLines_PDB2):
#     output1 = []
#     for i in range(len(output)):
#         pts1_idx = int(output[i][0])
#         temp_AminoAcid = splitLines_PDB1[pts1_idx][3]
#         charge1 = 0
#         temp = [pts1_idx]
#         temp.append([])
#         if temp_AminoAcid == "ARG" or temp_AminoAcid == "LYS":
#             charge1 = 1
#         elif (
#             temp_AminoAcid == "PHE"
#             or temp_AminoAcid == "TYR"
#             or temp_AminoAcid == "TRP"
#         ):
#             charge1 = -1
#         if charge1 != 0:
#             for j in range(len(output[i][1])):
#                 charge2 = 0
#                 pts2_idx = int(output[i][1][j])
#                 temp_AminoAcid = splitLines_PDB2[pts2_idx][3]
#                 if temp_AminoAcid == "ARG" or temp_AminoAcid == "LYS":
#                     charge2 = 1
#                 elif (
#                     temp_AminoAcid == "PHE"
#                     or temp_AminoAcid == "TYR"
#                     or temp_AminoAcid == "TRP"
#                 ):
#                     charge2 = -1
#                 total_charge = charge1 + charge2
#                 if total_charge == 0:
#                     # d1 = (points1[pts1_idx][0]-points2[pts2_idx][0])**2
#                     # d2 = (points1[pts1_idx][1]-points2[pts2_idx][1])**2
#                     # d3 = (points1[pts1_idx][2]-points2[pts2_idx][2])**2
#                     # d	=	math.sqrt(d1+d2+d3)
#                     # if d < dist:
#                     temp[1].append(str(pts2_idx))
#         if temp[1]:
#             output1.append(temp)
#     return output1
