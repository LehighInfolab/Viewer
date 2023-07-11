import getopt
import os
import math
import sys
import argparse
import shutil
import itertools

import numpy as np

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

sys.path.insert(1, "./lib")
# import PDBGreedySearch
import PDB_HB_parser
import hbondfinder_utils
import graph_utils

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
        required=True,
        metavar="InputPDB",
        help="Input PDB file to be compared. If only 1 file as input, then DiffBond will find bonds between all protein chains. If 2 files as input, then DiffBond will find bonds between the 2 PDB files.",
    )
    parser.add_argument("-o", nargs="?", metavar="OutputPDB", help="Output file name")

    parser.add_argument(
        "-c",
        nargs=2,
        metavar="Chains",
        help="If only one input file given, you can provide chains to calculate graph on only those 2 chains. Default = None, means calculate on all combination of chains.",
    )

    parser.add_argument(
        "-m",
        nargs="+",
        required=True,
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
    c_list = args["c"]
    d = args["d"]
    o = args["o"]
    return i_list, m_list, c_list, d, o


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

    temp = compareDist(p1, p2, dist)
    for edge in temp:
        if edge[0][4] == edge[1][4]:
            continue

        charge1 = get_charge_from_res(edge[0][3], edge[0][2])
        charge2 = get_charge_from_res(edge[1][3], edge[1][2])
        if charge1 == charge2:
            continue
        output.append(edge)

    ## this line created a bug where same charged residues within dist were considered as ionic bonds because charge checked first and then distance checked.
    # output = compareDist(p1, p2, dist)
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
def HB_processing(i_list, edges, outputFileName):
    if not edges:
        return None, None
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
        print("ERROR: File is empty. hbondfinder returned false.")
        os.remove("temp.pdb")
        return None, None

    try:
        hb_file_name = outputFileName + ".txt"
    except IndexError as error:
        print(
            "ERROR: Failed to process hydrogen bonds. Likely no hydrogens added to PDB."
        )
        return None, None
    print("RUNNING: Writing HBonds to: ", hb_file_name, "...")

    # If hbondfinder folder already contains a file with the same name, shutil.move will be unable to move the file and will not save your most recent run. Delete files and run again.
    try:
        shutil.copyfile("HBondFinder_temp.txt", "HBondFinder" + hb_file_name)
        # os.rename("HBondFinder_temp.txt", "HBondFinder" + hb_file_name)
        shutil.move("HBondFinder" + hb_file_name, "Results/" + outputFileName + "/")
    except OSError as error:
        print(
            "ERROR: Was not able to move HBondFinder file to hbond_data folder. Check to see that HBondFinder file does not already exist."
        )
        os.remove("HBondFinder" + hb_file_name)

    try:
        shutil.copyfile("hbonds_temp.txt", "hbonds" + hb_file_name)
        # os.rename("hbonds_temp.txt", "hbonds" + hb_file_name)
        shutil.move("hbonds" + hb_file_name, "Results/" + outputFileName + "/")
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

    return "HBondFinder" + hb_file_name, "hbonds" + hb_file_name


# Function for processing HB file from only 1 structure
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
        print("NOTE: Directory already exists. Adding files to existing directory")
    results_dir = "Results/" + outputFileName
    return results_dir


def make_pdb_dir(outputFileName):
    print("RUNNING: Duplicating PDB files to results folder...")
    try:
        os.mkdir("Results/" + outputFileName + "/pdb")
        print("--- Successfully created folder ---")
    except OSError as error:
        print("NOTE: Directory already exists. Adding files to existing directory")
    pdb_dir = "Results/" + outputFileName + "/pdb"
    return pdb_dir


def make_chain_comb_dir(outputFileName, chains):
    print("RUNNING: Making new folder for each combination of chains...")
    try:
        os.mkdir("Results/" + outputFileName + "/" + chains[0] + "_" + chains[1])
        print("--- Successfully created folder ---")
    except OSError as error:
        print("NOTE: Directory already exists. Adding files to existing directory")
    chain_dir = "Results/" + outputFileName + "/" + chains[0] + "_" + chains[1]
    return chain_dir


# Holds code to run the contact mode
def c_mode(PDB_data, dist, results_dir, use_visual):
    print("##### Searching contacts within " + str(dist) + "... #####")
    contact_edges = compareDist(PDB_data[0], PDB_data[1], dist)
    print(
        "--------------------------------------------------------------------------------------"
    )
    print("---CONTACT DISTANCE WITHIN " + str(dist) + " DISTANCE---")
    print(
        "--------------------------------------------------------------------------------------"
    )
    reformatted_edges = graph_utils.reformat_contact_ionic_for_graph(
        contact_edges, "contact"
    )
    # print(reformatted_edges)

    ## making and visualizing graph
    contact_graph, pos, color = graph_utils.make_graph(reformatted_edges)
    if use_visual:
        graph_utils.visualize_graph(
            contact_graph, pos, color, results_dir + "/contact_graph.png"
        )

    ## writing graph to file
    nx.write_multiline_adjlist(contact_graph, results_dir + "/contact_bonds.adjlist")
    nx.write_gml(contact_graph, results_dir + "/contact_bonds.gml")

    return contact_graph


# Holds code to run the ionic mode
def i_mode(PDB_data, dist, results_dir, use_visual):
    print("##### Searching ionic bonds... #####")
    ionic_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
    print(
        "--------------------------------------------------------------------------------------"
    )
    print("---IONIC BOND PREDICTIONS WITHIN " + str(dist) + " DISTANCE---")
    print(
        "--------------------------------------------------------------------------------------"
    )
    # print(ionic_edges)
    reformatted_edges = graph_utils.reformat_contact_ionic_for_graph(
        ionic_edges, "ionic"
    )
    print(reformatted_edges)

    ## making and visualizing graph
    ionic_graph, pos, color = graph_utils.make_graph(reformatted_edges)
    if use_visual:
        graph_utils.visualize_graph(
            ionic_graph, pos, color, results_dir + "/ionic_graph.png"
        )

    ## writing graph to file
    nx.write_multiline_adjlist(ionic_graph, results_dir + "/ionic_bonds.adjlist")
    nx.write_gml(ionic_graph, results_dir + "/ionic_bonds.gml")

    return ionic_graph


# Holds code to run the hbond mode
def h_mode(PDB_data, dist, results_dir, use_visual, i_list, outputFileName):
    print("##### Searching h-bonds... #####")
    edges_temp = compareDist(PDB_data[0], PDB_data[1], 3.5)

    print("##### Processing h-bonds... #####")
    HB_file, hb_file = HB_processing(i_list, edges_temp, outputFileName)

    if HB_file == None:
        print("ERROR: No bonds in contact distance to run hbondfinder.")
        return
    if hb_file == None:
        print("ERROR: No bonds in contact distance to run hbondfinder.")
        return

    print("##### Parsing hb finder file... #####")
    HB_lines = PDB_HB_parser.parse_file(
        "Results/" + outputFileName + "/" + HB_file, True, 1
    )
    hb_lines = PDB_HB_parser.parse_file(
        "Results/" + outputFileName + "/" + hb_file, True, 1
    )
    reformatted_edges = graph_utils.reformat_hbond_for_graph(HB_lines, hb_lines)
    # print("Reformatted edges", reformatted_edges)

    # print("##### continuing to parse hb finder file ... #####")
    # hbond_edges = hbondfinder_utils.parse_hbond_lines(hb_lines, True)

    print(
        "--------------------------------------------------------------------------------------"
    )
    print("---H-BOND PREDICTIONS THAT MEET HBONDFINDER CRITERIA---")
    print(
        "--------------------------------------------------------------------------------------"
    )
    print(reformatted_edges)

    ## making and visualizing graph
    hbond_graph, pos, color = graph_utils.make_digraph_hbond(reformatted_edges)

    if use_visual:
        graph_utils.visualize_graph(
            hbond_graph, pos, color, results_dir + "/hbond_graph.png"
        )

    ## writing graph to file
    nx.write_multiline_adjlist(hbond_graph, results_dir + "/hbonds.adjlist")
    nx.write_gml(hbond_graph, results_dir + "/hbonds.gml")

    return hbond_graph


def compareDistAdj(contact, points1, points2, dist):
    output = []
    chain1 = points1[0][4]
    chain2 = points2[0][4]
    for i in contact:
        if i[0][4] == chain1:
            A1 = i[0]
            for j in points1:
                if A1 == j:
                    continue
                d1 = (float(A1[6]) - float(j[6])) ** 2
                d2 = (float(A1[7]) - float(j[7])) ** 2
                d3 = (float(A1[8]) - float(j[8])) ** 2
                d = math.sqrt(d1 + d2 + d3)
                if d < dist:
                    edge = [A1, j, d]
                    output.append(edge)
            A2 = i[1]
            for j in points2:
                if A2 == j:
                    continue
                d1 = (float(A2[6]) - float(j[6])) ** 2
                d2 = (float(A2[7]) - float(j[7])) ** 2
                d3 = (float(A2[8]) - float(j[8])) ** 2
                d = math.sqrt(d1 + d2 + d3)
                if d < dist:
                    edge = [A2, j, d]
                    output.append(edge)
        elif i[1][4] == chain1:
            A1 = i[1]
            for j in points1:
                if A1 == j:
                    continue
                d1 = (float(A1[6]) - float(j[6])) ** 2
                d2 = (float(A1[7]) - float(j[7])) ** 2
                d3 = (float(A1[8]) - float(j[8])) ** 2
                d = math.sqrt(d1 + d2 + d3)
                if d < dist:
                    edge = [A1, j, d]
                    output.append(edge)
            A2 = i[0]
            for j in points2:
                if A2 == j:
                    continue
                d1 = (float(A2[6]) - float(j[6])) ** 2
                d2 = (float(A2[7]) - float(j[7])) ** 2
                d3 = (float(A2[8]) - float(j[8])) ** 2
                d = math.sqrt(d1 + d2 + d3)
                if d < dist:
                    edge = [A2, j, d]
                    output.append(edge)
    return output


def a_mode(PDB_data, dist, results_dir, use_visual):
    print("##### Searching contacts adjacent to bonds #####")
    contact_edges = compareDistIonic(PDB_data[0], PDB_data[1], dist)
    adj_edges = compareDistAdj(contact_edges, PDB_data[0], PDB_data[1], dist)
    print(
        "--------------------------------------------------------------------------------------"
    )
    print("---ADJ BONDS WITHIN " + str(dist) + " DISTANCE OF EXISTING BONDS---")
    print(
        "--------------------------------------------------------------------------------------"
    )
    reformatted_edges = graph_utils.reformat_contact_ionic_for_graph(adj_edges, "adj")
    # print(reformatted_edges)

    ## making and visualizing graph
    adj_graph, pos, color = graph_utils.make_graph(reformatted_edges)
    if use_visual:
        graph_utils.visualize_graph(
            adj_graph, pos, color, results_dir + "/adj_graph.png"
        )

    ## writing graph to file
    nx.write_multiline_adjlist(adj_graph, results_dir + "/adj_bonds.adjlist")
    nx.write_gml(adj_graph, results_dir + "/adj_bonds.gml")


def s_mode(i_graph, h_graph, results_dir, use_visual):

    if i_graph == None or h_graph == None:
        return
    s_graph = nx.intersection(i_graph, h_graph)
    print(s_graph)

    ## writing graph to file
    nx.write_multiline_adjlist(s_graph, results_dir + "/salt_bridges.adjlist")
    nx.write_gml(s_graph, results_dir + "/salt_bridges_bonds.gml")

    return s_graph


def main():
    i_list, mode, c_list, dist, outputFileName = parseArg()

    if dist == None:
        dist = 5.0
    else:
        dist = float(dist)

    # Set output file name if no name was given in args
    if outputFileName == None:
        special_characters = ["\\", "/"]
        outputFileName = "Result"
        for i in i_list:
            temp = i
            for s in special_characters:
                temp = str(temp.split(s)[-1])
            outputFileName = outputFileName + "_" + str(temp.split(".")[-2])
        if dist != 5.0:
            outputFileName = outputFileName + "_" + str(dist)

    use_visual = False
    PDB_data_list = []
    chains_comb = []

    # Different process for one input file given vs 2 input files given.
    if len(i_list) == 1:
        for i in i_list:
            PDB_data = PDB_HB_parser.parse_PDB_file(i)
            if not PDB_data:
                print("No data in PDB chain.")
            chains_data = PDB_HB_parser.split_PDB_chain(PDB_data)
            if c_list != None:
                chains_comb.append(c_list)
                PDB_data = []
                PDB_data.append(chains_data[c_list[0]])
                PDB_data.append(chains_data[c_list[1]])
                PDB_data_list.append(PDB_data)

            else:
                chains_comb = list(itertools.combinations(list(chains_data.keys()), 2))
                for c in chains_comb:
                    PDB_data = []
                    PDB_data.append(chains_data[c[0]])
                    PDB_data.append(chains_data[c[1]])
                    PDB_data_list.append(PDB_data)

    elif len(i_list) == 2:
        PDB_data = []
        for i in i_list:
            data = PDB_HB_parser.parse_PDB_file(i)
            if not data:
                print("No data found in PDB files.")
                return
            PDB_data.append(data)
        PDB_data_list.append(PDB_data)

    # Create folder for results to be stored. If folder already exists, then skip.
    print(
        '--- Results will be printed to "',
        outputFileName,
        '" in Results folder ---',
    )
    root_results_dir = make_results_dir(outputFileName)
    pdb_dir = make_pdb_dir(outputFileName)
    for i in i_list:
        shutil.copy(i, pdb_dir)

    for i in range(len(PDB_data_list)):
        results_dir = None
        if len(i_list) == 2:
            results_dir = root_results_dir
        if len(i_list) == 1:
            print(
                "----------------- Computing for the following chains -----------------\n",
                chains_comb[i],
            )
            if len(PDB_data_list) > 1:
                chain_dir = make_chain_comb_dir(outputFileName, chains_comb[i])
                results_dir = chain_dir
            elif len(PDB_data_list) == 1:
                results_dir = root_results_dir

        # "Cache" the edges if they have been calculated if a mode requires multiple different bonds to calculate eg. salt bridges, graphs
        contact_edges = []
        ionic_edges = []
        hbond_edges = []

        # Switch statement for all bond functions
        for m in mode:
            c_graph = None
            i_graph = None
            h_graph = None
            if m == "c":
                c_mode(PDB_data_list[i], dist, results_dir, use_visual)

            elif m == "i":
                i_mode(PDB_data_list[i], dist, results_dir, use_visual)

            elif m == "h":
                h_mode(
                    PDB_data_list[i],
                    dist,
                    results_dir,
                    use_visual,
                    i_list,
                    outputFileName,
                )

            elif m == "a":
                a_mode(PDB_data_list[i], dist, results_dir, use_visual)

            elif m == "g":
                if contact_edges == []:
                    c_graph = c_mode(PDB_data_list[i], dist, results_dir, use_visual)

                if ionic_edges == []:
                    i_graph = i_mode(PDB_data_list[i], dist, results_dir, use_visual)

                if hbond_edges == []:
                    h_graph = h_mode(
                        PDB_data_list[i],
                        dist,
                        results_dir,
                        use_visual,
                        i_list,
                        outputFileName,
                    )

                s_mode(i_graph, h_graph, results_dir, use_visual)

                ## making combined ionic and hbond graphs
                # TODO: FIX THIS
                # new_edges = reformat_contact_ionic_for_graph(ionic_edges)
                # for i in hbond_edges:
                #     new_edges.append(i)
                # print(
                #     "--------------------------------------------------------------------------------------"
                # )
                # print("---IONIC + HBONDS---")
                # print(
                #     "--------------------------------------------------------------------------------------"
                # )
                # print(new_edges)
                # ionic_hbond_graph, pos = make_graph(new_edges)

                # if use_visual:
                #     visualize_graph(
                #         ionic_hbond_graph, pos, results_dir + "/ionic+hbonds_graph.png"
                #     )

                # ## write graphs
                # nx.write_multiline_adjlist(
                #     ionic_hbond_graph, results_dir + "/ionic+hbonds.adjlist"
                # )
                # nx.write_gml(ionic_hbond_graph, results_dir + "/ionic+hbonds.gml")


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
