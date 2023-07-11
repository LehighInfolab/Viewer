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


# Util function just for reformatting edge format outputted by ionic bond and salt bridge edges so that they contain only [chain letter + AA number of donors, chain letter + AA number of acceptors, distance]
def reformat_contact_ionic_for_graph(edges, bond_type):
    new_edges = []
    for edge in edges:
        a1 = [
            edge[0][4].strip(),
            edge[0][5].strip(),
            edge[0][3].strip(),
            [float(edge[0][6]), float(edge[0][7]), float(edge[0][8])],
        ]
        a2 = [
            edge[1][4].strip(),
            edge[1][5].strip(),
            edge[1][3].strip(),
            [float(edge[1][6]), float(edge[1][7]), float(edge[1][8])],
        ]
        e = [bond_type, round(edge[2], 2)]
        reformat_edge = [a1, a2, e]
        if reformat_edge not in new_edges:
            new_edges.append(reformat_edge)
    return new_edges


# Util function just for reformatting edge format outputted by ionic bond and salt bridge edges so that they contain only [chain letter + AA number of donors, chain letter + AA number of acceptors, distance]
def reformat_hbond_for_graph(HB_edges, hb_coords):
    coords = []
    for line in hb_coords:
        if line[0] == "#NUMBER_OF_HBONDS":
            break
        else:
            AA = [line[0].strip(), line[2].strip(), line[1].strip(), line[3].strip()]
            coord = [
                float(line[5].strip()),
                float(line[6].strip()),
                float(line[7].strip()),
            ]
            coords.append([AA, coord])

    edges = []
    for edge in HB_edges:
        ## get coord data from hb_coords assigned to the correct amino acids
        for coord in coords:
            if (
                edge[0] == coord[0][0]
                and edge[1] == coord[0][1]
                and edge[2] == coord[0][2]
                and edge[3] == coord[0][3]
            ):
                edge.append(coord[1])
            if (
                edge[4] == coord[0][0]
                and edge[5] == coord[0][1]
                and edge[6] == coord[0][2]
                and edge[7] == coord[0][3]
            ):
                edge.append(coord[1])
        a1 = [edge[0].strip(), edge[1].strip(), edge[2].strip(), edge[-2], "donor"]
        a2 = [edge[4].strip(), edge[5].strip(), edge[6].strip(), edge[-1], "acceptor"]
        e = ["hbond", round(float(edge[8]), 2)]
        reformat_edge = [a1, a2, e]
        if reformat_edge not in edges:
            edges.append(reformat_edge)

    return edges


# Util function for making a networkx graph object from a list of edges. Automatically puts into bipartite format.
def make_graph_hbond(edges):

    G = nx.Graph()
    pos = nx.get_node_attributes(G, "pos")
    color = nx.get_node_attributes(G, "color")

    # if edges is empty, return
    if not edges:
        return G, pos

    for edge in edges:
        ## added edge labels here
        G.add_edge(edge[0][1], edge[1][1], bond_type=edge[2][0], weight=edge[2][1])

        ## adding node labels
        G.nodes[edge[0][1]]["AA"] = edge[0][2]
        G.nodes[edge[1][1]]["AA"] = edge[1][2]

        G.nodes[edge[0][1]]["coord"] = edge[0][3]
        G.nodes[edge[1][1]]["coord"] = edge[1][3]

        G.nodes[edge[0][1]]["chain"] = edge[0][0]
        G.nodes[edge[1][1]]["chain"] = edge[1][0]

        ## if graph is for hbonds, add a donor acceptor node label
        edge1_val = G.nodes[edge[0][1]].get("hbond")
        edge2_val = G.nodes[edge[1][1]].get("hbond")
        if edge1_val == None:
            G.nodes[edge[0][1]]["hbond"] = edge[0][4]
        if edge2_val == None:
            G.nodes[edge[1][1]]["hbond"] = edge[0][4]
        if edge1_val != None:
            if edge1_val != edge[0][4]:
                G.nodes[edge[0][1]]["hbond"] = ["donor", "acceptor"]
        if edge2_val != None:
            if edge2_val != edge[1][4]:
                G.nodes[edge[1][1]]["hbond"] = ["donor", "acceptor"]

        ## use atom positions for position in figures
        pos[edge[0][1]] = np.array([edge[0][3][0], edge[0][3][1]])
        pos[edge[1][1]] = np.array([edge[1][3][0], edge[1][3][1]])

        ## use edge to indicate
        color[edge[0][1]] = (0, 1, 1)
        color[edge[1][1]] = (1, 0.3, 0.3)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    ## draw position of nodes on one side of interface separate from other side
    # pos = nx.drawing.layout.bipartite_layout(G, left_nodes)

    return G, pos, color


# Util function for making a networkx graph object from a list of edges. Automatically puts into bipartite format.
def make_digraph_hbond(edges):

    G = nx.DiGraph()
    pos = nx.get_node_attributes(G, "pos")
    color = nx.get_node_attributes(G, "color")

    # if edges is empty, return
    if not edges:
        return G, pos

    for edge in edges:
        ## added edge labels here
        G.add_edge(edge[0][1], edge[1][1], bond_type=edge[2][0], weight=edge[2][1])

        ## adding node labels
        G.nodes[edge[0][1]]["AA"] = edge[0][2]
        G.nodes[edge[1][1]]["AA"] = edge[1][2]

        G.nodes[edge[0][1]]["coord"] = edge[0][3]
        G.nodes[edge[1][1]]["coord"] = edge[1][3]

        G.nodes[edge[0][1]]["chain"] = edge[0][0]
        G.nodes[edge[1][1]]["chain"] = edge[1][0]

        ## if graph is for hbonds, add a donor acceptor node label
        edge1_val = G.nodes[edge[0][1]].get("hbond")
        edge2_val = G.nodes[edge[1][1]].get("hbond")
        if edge1_val == None:
            G.nodes[edge[0][1]]["hbond"] = edge[0][4]
        if edge2_val == None:
            G.nodes[edge[1][1]]["hbond"] = edge[0][4]
        if edge1_val != None:
            if edge1_val != edge[0][4]:
                G.nodes[edge[0][1]]["hbond"] = ["donor", "acceptor"]
        if edge2_val != None:
            if edge2_val != edge[1][4]:
                G.nodes[edge[1][1]]["hbond"] = ["donor", "acceptor"]

        ## use atom positions for position in figures
        pos[edge[0][1]] = np.array([edge[0][3][0], edge[0][3][1]])
        pos[edge[1][1]] = np.array([edge[1][3][0], edge[1][3][1]])

        ## use edge to indicate
        color[edge[0][1]] = (0, 1, 1)
        color[edge[1][1]] = (1, 0.3, 0.3)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    ## draw position of nodes on one side of interface separate from other side
    # pos = nx.drawing.layout.bipartite_layout(G, left_nodes)

    return G, pos, color


# Util function for making a networkx graph object from a list of edges. Automatically puts into bipartite format.
def make_graph(edges):
    G = nx.Graph()
    pos = nx.get_node_attributes(G, "pos")
    color = nx.get_node_attributes(G, "color")

    # if edges is empty, return
    if not edges:
        return G, [], []

    ## make sure all nodes on left side are from the same chain
    left_chain = edges[0][0][0]
    left_nodes = []

    for edge in edges:
        same_chain = False
        ## if the first node, edge[0], is not on the same chain as left_chain, then switch positions of the nodes. Use flipped boolean to keep track if edges have been switched

        if edge[0][0] != left_chain:
            temp = edge[0]
            edge[0] = edge[1]
            edge[1] = temp

        ## added edge labels here
        G.add_edge(edge[0][1], edge[1][1], bond_type=edge[2][0], weight=edge[2][1])

        ## adding node labels
        G.nodes[edge[0][1]]["AA"] = edge[0][2]
        G.nodes[edge[1][1]]["AA"] = edge[1][2]

        G.nodes[edge[0][1]]["coord"] = edge[0][3]
        G.nodes[edge[1][1]]["coord"] = edge[1][3]

        G.nodes[edge[0][1]]["chain"] = edge[0][0]
        G.nodes[edge[1][1]]["chain"] = edge[1][0]

        ## use atom positions for position in figures
        pos[edge[0][1]] = np.array([edge[0][3][0], edge[0][3][1]])
        pos[edge[1][1]] = np.array([edge[1][3][0], edge[1][3][1]])

        ## use edge to indicate color
        if not same_chain:
            color[edge[0][1]] = (0, 1, 1)
            color[edge[1][1]] = (1, 0.3, 0.3)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    ## draw position of nodes on one side of interface separate from other side
    # pos = nx.drawing.layout.bipartite_layout(G, left_nodes)

    return G, pos, color


# Util function for visualizing graph
def visualize_graph(G, pos, color, save_dir_name):
    if nx.is_empty(G):
        return
    print(G)
    ## set up drawing of graphs
    plt.subplot(121)
    nx.draw(G, with_labels=True, node_color=list(color.values()), pos=pos)

    edge_labels = nx.get_edge_attributes(G, "bond_type")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)

    plt.savefig(save_dir_name, bbox_inches="tight")
    plt.show()
