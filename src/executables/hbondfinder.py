#Program Capabilities:
#       - Find H-Bonds by building grid of acceptors, and querying
#         on each donor atom
#       - Run through the process of building grids of varying box 
#         dimensions
#       - Can handle batches of pdb files at a time as input


#Author: Omar Ahmed
#Last Modified: 10/21/2019
import sys
import random
import time
import warnings
import json
import xlwt
import math
import getopt
from glob import glob
from Bio.PDB import Selection
from Bio.PDB.vectors import calc_angle
from Bio import BiopythonWarning
from Bio.PDB import Atom
from Bio.PDB.PDBParser import PDBParser


#Helper Methods -----------------------------------------------------------------------------------------------------------------

#Loads JSON file into Python Dictionary Object
def get_acceptor_donor_dictionary():
    acceptor_donor_file = open(dict_json_file, "r")
    acceptor_donor_string = acceptor_donor_file.read()
    acceptor_donor_dict = json.loads(acceptor_donor_string)

    return acceptor_donor_dict

#These two methods generate list of acceptors and donors by the long way, inefficient way, by using if statements
def getListOfAcceptorAtoms_OLD(PDB_file):
    structure = parser.get_structure("structure_id", PDB_file)
    #Makes a list of acceptors
    acceptorList = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    #Atoms within Side Chains
                    if atom.get_name() == "OD1" and residue.get_resname() == "ASN" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OD1" and residue.get_resname() == "ASP" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OD2" and residue.get_resname() == "ASP" :
                        acceptorList.append(atom)
                    if atom.get_name() == "SG" and residue.get_resname() == "CYS" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OE1" and residue.get_resname() == "GLU" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OE2" and residue.get_resname() == "GLU" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OE1" and residue.get_resname() == "GLN" :
                        acceptorList.append(atom)
                    if atom.get_name() == "ND1" and residue.get_resname() == "HIS" :
                        acceptorList.append(atom)
                    if atom.get_name() == "SD" and residue.get_resname() == "MET" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OG" and residue.get_resname() == "SER" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OG1" and residue.get_resname() == "THR" :
                        acceptorList.append(atom)
                    if atom.get_name() == "OH" and residue.get_resname() == "TYR" :
                        acceptorList.append(atom) 

    return acceptorList

def getListOfDonorAndHydrogenAtoms_OLD(PDB_file):
    structure = parser.get_structure("structure_id", PDB_file)
    donorList = []
    donor_hydrogen_list = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    #Adding Donor Atoms to Donor List
                    if atom.get_name() == "NE" and residue.get_resname() == "ARG" :
                    #   print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NH1" and residue.get_resname() == "ARG" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NH2" and residue.get_resname() == "ARG" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "SG" and residue.get_resname() == "CYS" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NE2" and residue.get_resname() == "GLN" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NE2" and residue.get_resname() == "HIS" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "ND1" and residue.get_resname() == "HIS" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NZ" and residue.get_resname() == "LYS" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "OG" and residue.get_resname() == "SER" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "OG1" and residue.get_resname() == "THR" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "OH" and residue.get_resname() == "TYR" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "NE1" and residue.get_resname() == "TRP" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                    if atom.get_name() == "ND2" and residue.get_resname() == "ASN" :
                        #print(atom.get_name()  +   "   "  + atom.get_parent().get_resname())
                        donorList.append(atom)
                
                    #Going through Donor List and seeing if the hydrogen belongs to any unpaired donors
                    if (atom.get_name())[0] == "H":
                        for potentialDonor in donorList:
                            if potentialDonor.get_parent() == residue:
                                if potentialDonor.get_name() == "NE" and potentialDonor.get_parent().get_resname() == "ARG" and atom.get_name() == "HE":
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NH1" and potentialDonor.get_parent().get_resname() == "ARG" and (atom.get_name() == "HH11" or atom.get_name() == "HH12"):
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NH2" and potentialDonor.get_parent().get_resname() == "ARG" and (atom.get_name() == "HH21" or atom.get_name() == "HH22"):
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "SG" and potentialDonor.get_parent().get_resname() == "CYS" and atom.get_name() == "HG":
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NE2" and potentialDonor.get_parent().get_resname() == "GLN" and (atom.get_name() == "HE21" or atom.get_name() == "HE22") :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NE2" and potentialDonor.get_parent().get_resname() == "HIS" and atom.get_name() == "HE2" :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    donorList.remove(potentialDonor)
                                #Does this nitrogen have a hydrogen bonded to it?
                                #if potentialDonor.get_name() == "ND1" and potentialDonor.get_parent().get_resname() == "HIS" and atom.get_name() == "HE2" :
                                #   donor_hydrogen_list.append([potentialDonor, atom])
                                #  donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NZ" and potentialDonor.get_parent().get_resname() == "LYS" and (atom.get_name() == "HZ1" or atom.get_name() == "HZ2" or atom.get_name() == "HZ3" ) :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "OG" and potentialDonor.get_parent().get_resname() == "SER" and atom.get_name() == "HG" :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "OG1" and potentialDonor.get_parent().get_resname() == "THR" and atom.get_name() == "HG1" :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "OH" and potentialDonor.get_parent().get_resname() == "TYR" and atom.get_name() == "HH" :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "NE1" and potentialDonor.get_parent().get_resname() == "TRP" and atom.get_name() == "HE1" :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    donorList.remove(potentialDonor)
                                if potentialDonor.get_name() == "ND2" and potentialDonor.get_parent().get_resname() == "ASN" and (atom.get_name() == "HD21" or atom.get_name() == "HD22") :
                                    donor_hydrogen_list.append([potentialDonor, atom])
                                    #print(str(residue.get_resname()) + str([potentialDonor, atom]))
                                    #donorList.remove(potentialDonor)          
    return donor_hydrogen_list

#These two methods generate lists of acceptors and donors using
#the Python dictionary that encodes all the donors and acceptors
def getListOfAcceptorAtoms(PDB_file):
    acceptor_donor_dict = get_acceptor_donor_dictionary()
    structure = parser.get_structure("structure_id", PDB_file)
    acceptorList1 = []

    #Iterates through each residue in structure
    for model in structure:
        for chain in model:
            for residue in chain:
                res_str = residue.get_resname()              
                #Checks if residue is present in acceptor/donor JSON file
                if res_str in acceptor_donor_dict:
                    for key in acceptor_donor_dict[res_str]:
                        if key[0] == "A" and key[1] != "A":
                            #Gets acceptor atom name, and finds it in the residue to add to list
                            acceptor_str = acceptor_donor_dict[res_str][key]
                            for atom in residue:
                                if atom.get_name() == acceptor_str:
                                    acceptorList1.append(atom)
    return acceptorList1

def getListOfDonorAndHydrogenAtoms(PDB_file):
    acceptor_donor_dict = get_acceptor_donor_dictionary()
    structure = parser.get_structure("structure_id", PDB_file)
    donorList1 = []
    #Iterates through all residues in structure
    for model in structure:
        for chain in model:
            for residue in chain:
                res_str = residue.get_resname()
                if res_str in acceptor_donor_dict:

                    #Checks if residue is in acceptor/donor JSON file
                    for key in acceptor_donor_dict[res_str]:
                        if key[0] == "D":
                            donor_str = acceptor_donor_dict[res_str][key]
                            donor_num = int(key[1])
                            
                            #Finds hydrogen that corresponds to a specific donor atom
                            for hydrogen_key in acceptor_donor_dict[res_str]:
                                if hydrogen_key[0] == "H":
                                    hydrogen_str = acceptor_donor_dict[res_str][hydrogen_key]
                                    hydrogen_num = int(hydrogen_key[1])
                                    
                                    #When it finds the hydrogen atom name corresponding to the donor ...
                                    if (hydrogen_num == donor_num):
                                        #just initializes these atom variables
                                        for atom in residue:
                                            donor_atom = atom
                                            hydrogen_atom = atom
                                        #finds the donor and hydrogen atom objects
                                        hydrogen_found = 0
                                        donor_found = 0
                                        #Tries to find the donor and hydrogen atom in actual file
                                        for atom in residue:
                                            if atom.get_name() == donor_str:
                                                donor_atom = atom
                                                donor_found = 1
                                            if atom.get_name() == hydrogen_str:
                                                hydrogen_atom = atom
                                                hydrogen_found = 1
                                        #Appends a warning when either hydrogen or donor was not found
                                        if hydrogen_found == 0:
                                            warnings_list.append("WARNING: " + hydrogen_str + " was not found in " + res_str)
                                        if donor_found == 0:
                                            warnings_list.append("WARNING: " + donor_str + " was not found in " + res_str)
                                        if donor_atom.get_parent() == hydrogen_atom.get_parent() and donor_found == 1 and hydrogen_found == 1:
                                            donorList1.append([donor_atom, hydrogen_atom])
    return donorList1

#Appends oxygens in water molecules that could act as donor atoms in hydrogen bonds
def addDonorOxygenFromWaters(PDB_File, donor_hydrogen_list):
    acceptor_donor_dict = get_acceptor_donor_dictionary()
    structure = parser.get_structure("structure_id", PDB_File)

    #Iterates through all residues in structure
    for model in structure:
        for chain in model:
            for residue in chain:

                res_str = residue.get_resname()
                residue_id = residue.get_id()
                hetfield = residue_id[0]

                #It's a water molecule
                if hetfield == "W":
                    for key in acceptor_donor_dict[res_str]:
                        if key[0] == "D":
                            donor_str = acceptor_donor_dict[res_str][key]
                            for atom in residue:
                                if atom.get_name() == donor_str:
                                    #Just putting atom as placeholder since PDB usually doesn't have Hydrogens for water
                                    donor_hydrogen_list.append([atom, atom])
    return donor_hydrogen_list


#Returns number of boxes in certain dimension, using global variable for box dimensions  
def getBoxDimension(dim):
    if dim % DESIRED_BOX_DIMENSTION != 0:
        boxDim = int((dim // DESIRED_BOX_DIMENSTION) + 1)
    else:
        boxDim = int(dim / DESIRED_BOX_DIMENSTION)
    return boxDim

#Returns number of boxes in certain dimension, using parameter for box dimension
def getBoxDimension_DifferentDimensions(dim, BOX_DIMENSION):
    if dim % BOX_DIMENSION != 0:
        boxDim = int((dim // BOX_DIMENSION) + 2)
    else:
        boxDim = int(dim / BOX_DIMENSION) + 1
    return boxDim


def getGridBoxNumber(atom):
    x_coord, y_coord, z_coord = atom.get_coord()
    return getGridBoxNumberWithCoords(x_coord, y_coord, z_coord)
    
def getGridBoxNumberWithCoords(x_coord, y_coord, z_coord):
      
    block_num = int(z_block_num * (xBoxDim * yBoxDim) + y_block_num * (xBoxDim) + x_block_num)

def getBoxNumbers_forRandomTesting(x_coord, y_coord, z_coord):
    x_coord_pos = adjust_x_coord_to_Grid(x_coord)
    y_coord_pos = adjust_y_coord_to_Grid(y_coord)
    z_coord_pos = adjust_z_coord_to_Grid(z_coord)

    x_block_num = x_coord_pos // DESIRED_BOX_DIMENSTION
    y_block_num = y_coord_pos // DESIRED_BOX_DIMENSTION
    z_block_num = z_coord_pos // DESIRED_BOX_DIMENSTION

    return [x_block_num, y_block_num, z_block_num]


#These methods make sure a coordinate has not gone outside the range
#in that specific dimension, using global variables
def doubleCheck_x_boundaries(x_coord):
    if x_coord < 0:
        return 0.0
    if x_coord > xdim:
        return xdim
    return x_coord

def doubleCheck_y_boundaries(y_coord):
    if y_coord < 0:
        return 0.0
    if y_coord > ydim:
        return ydim
    return y_coord

def doubleCheck_z_boundaries(z_coord):
    if z_coord < 0:
        return 0.0
    if z_coord > zdim:
        return zdim
    return z_coord


#These methods make sure a coordinate has not gone outside the range
#in that specific dimension, using parameter as dimension
def doubleCheck_x_boundaries_General(x_coord, xdimension):
    if x_coord < 0:
        return 0.0
    if x_coord > xdimension:
        return xdimension
    return x_coord   

def doubleCheck_y_boundaries_General(y_coord, ydimension):
    if y_coord < 0:
        return 0.0
    if y_coord > ydimension:
        return ydimension
    return y_coord   

def doubleCheck_z_boundaries_General(z_coord, zdimension):
    if z_coord < 0:
        return 0.0
    if z_coord > zdimension:
        return zdimension
    return z_coord

#These methods make sure a box number has not gone outside the range
#of boxes in that specific dimension
def doubleCheck_x_BoxBoundaries_General(xBoxNum, xBoxDimension):
    if xBoxNum < 0:
        return 0
    if xBoxNum >= xBoxDimension:
        return (xBoxDimension-1)
    return xBoxNum

def doubleCheck_y_BoxBoundaries_General(yBoxNum, yBoxDimension):
    if yBoxNum < 0:
        return 0
    if yBoxNum >= yBoxDimension:
        return (yBoxDimension-1)
    return yBoxNum

def doubleCheck_z_BoxBoundaries_General(zBoxNum, zBoxDimension):
    if zBoxNum < 0:
        return 0
    if zBoxNum >= zBoxDimension:
        return (zBoxDimension-1)
    return zBoxNum


#Adjusts the coordinate of an atom to make sure it is within the Grid    
def adjust_x_coord_to_Grid(x_coord):
    if min_x_coord < 0:
        x_coord_pos = x_coord + (-min_x_coord)
    else:
        x_coord_pos = x_coord - min_x_coord
    return x_coord_pos

def adjust_y_coord_to_Grid(y_coord):
    if min_y_coord < 0:
        y_coord_pos = y_coord + (-min_y_coord)
    else:
        y_coord_pos = y_coord - min_y_coord
    return y_coord_pos

def adjust_z_coord_to_Grid(z_coord):
    if min_z_coord < 0:
        z_coord_pos = z_coord + (-min_z_coord)
    else:
        z_coord_pos = z_coord - min_z_coord
    return z_coord_pos

#Adjusts the coordinate of an atom to be within the grid, however
#these methods are general since they don't use global variables
def adjust_x_coord_to_Grid_General(x_coord, min_x_coordinate):
    if min_x_coordinate < 0:
        x_coord_pos = x_coord + (-min_x_coordinate)
    else:
        x_coord_pos = x_coord - min_x_coordinate
    return x_coord_pos

def adjust_y_coord_to_Grid_General(y_coord, min_y_coordinate): 
    if min_y_coordinate < 0:
        y_coord_pos = y_coord + (-min_y_coordinate)
    else:
        y_coord_pos = y_coord - min_y_coordinate
    return y_coord_pos

def adjust_z_coord_to_Grid_General(z_coord, min_z_coordinate):
    if min_z_coordinate < 0:
        z_coord_pos = z_coord + (-min_z_coordinate)
    else:
        z_coord_pos = z_coord - min_z_coordinate
    return z_coord_pos


#Adds a buffer block in a certain direction for the range search
def add_buffer_block_in_x_direction(max_x_block, min_x_block):
    if (max_x_block + 1) < xBoxDim:
        max_x_block = max_x_block + 1
    if (min_x_block - 1) >= 0:
        min_x_block = min_x_block - 1
    return [max_x_block, min_x_block]

def add_buffer_block_in_y_direction(max_y_block, min_y_block):
    if (max_y_block + 1) < yBoxDim:
        max_y_block = max_y_block + 1
    if (min_y_block - 1) >= 0:
        min_y_block = min_y_block - 1
    return [max_y_block, min_y_block]

def add_buffer_block_in_z_direction(max_z_block, min_z_block):
    if (max_z_block + 1) < zBoxDim:
        max_z_block = max_z_block + 1
    if (min_z_block - 1) >= 0:
        min_z_block = min_z_block - 1
    return [max_z_block, min_z_block]


#Adds a buffer block in a certain direction, however these methods
#do not rely on any global variables
def add_buffer_block_in_x_direction_DIFFERENT_DIMENSIONS(max_x_block, min_x_block, xBoxDim):
    if (max_x_block + 1) < xBoxDim:
        max_x_block = max_x_block + 1
    if (min_x_block - 1) >= 0:
        min_x_block = min_x_block - 1
    return [max_x_block, min_x_block]

def add_buffer_block_in_y_direction_DIFFERENT_DIMENSIONS(max_y_block, min_y_block, yBoxDim):
    if (max_y_block + 1) < yBoxDim:
        max_y_block = max_y_block + 1
    if (min_y_block - 1) >= 0:
        min_y_block = min_y_block - 1
    return [max_y_block, min_y_block]

def add_buffer_block_in_z_direction_DIFFERENT_DIMENSIONS(max_z_block, min_z_block, zBoxDim):
    if (max_z_block + 1) < zBoxDim:
        max_z_block = max_z_block + 1
    if (min_z_block - 1) >= 0:
        min_z_block = min_z_block - 1
    return [max_z_block, min_z_block]


#Original buildGrid method, relies on global variables
def buildGrid(list_of_atoms):
    for atom in list_of_atoms:
                x_coord, y_coord, z_coord = atom.get_coord()

                #Now turn all coordinates to positive values by adding the minus value of dimension
                x_coord_pos = adjust_x_coord_to_Grid(x_coord)
                y_coord_pos = adjust_y_coord_to_Grid(y_coord)
                z_coord_pos = adjust_z_coord_to_Grid(z_coord)

                #Now, lets determine which block the atom will go into.
                x_block_num = x_coord_pos // DESIRED_BOX_DIMENSTION
                y_block_num = y_coord_pos // DESIRED_BOX_DIMENSTION
                z_block_num = z_coord_pos // DESIRED_BOX_DIMENSTION

                #Now, lets append this atom to the correct block
                grid[int(z_block_num * (xBoxDim * yBoxDim) + y_block_num * (xBoxDim) + x_block_num)].append(atom)

#buildGrid for random testing of points, method doesn't rely on any global variables
def buildGrid_RandomTesting(list_of_coordinates, testGrid, BOX_DIMENSION, lattice_dimensions ):

    xBoxDimension, yBoxDimension, zBoxDimension = lattice_dimensions

    for coords in list_of_coordinates:
                x_coord, y_coord, z_coord = coords

                #Now, lets determine which block the atom will go into.
                x_block_num = x_coord // BOX_DIMENSION
                y_block_num = y_coord // BOX_DIMENSION
                z_block_num = z_coord // BOX_DIMENSION

                #Now, lets append this atom to the correct block
                testGrid[int(z_block_num * (xBoxDimension * yBoxDimension) + y_block_num * (xBoxDimension) + x_block_num)].append(coords)
    return testGrid

#buildGrid for General Cases, method doesn't rely on any global variables
def buildGrid_DifferentSizes(list_of_atoms, testGrid, BOX_DIMENSION, lattice_dimensions, min_coordinates):
    xBoxDimension, yBoxDimension, zBoxDimension = lattice_dimensions
    for atom in list_of_atoms:
                x_coord, y_coord, z_coord = atom.get_coord()
                
                min_x_coord, min_y_coord, min_z_coord = min_coordinates

                #Now turn all coordinates to positive values by adding the minus value of dimension
                x_coord_pos = adjust_x_coord_to_Grid_General(x_coord, min_x_coord)
                y_coord_pos = adjust_y_coord_to_Grid_General(y_coord, min_y_coord)
                z_coord_pos = adjust_z_coord_to_Grid_General(z_coord, min_z_coord)
                
                #Now, lets determine which block the atom will go into.
                x_block_num = x_coord_pos // BOX_DIMENSION
                y_block_num = y_coord_pos // BOX_DIMENSION
                z_block_num = z_coord_pos // BOX_DIMENSION
                
                #Now, lets append this atom to the correct block
                testGrid[int(z_block_num * (xBoxDimension * yBoxDimension) + y_block_num * (xBoxDimension) + x_block_num)].append(atom)
    return testGrid

#Original queryBox method, relies on global variables
def queryBoxOnAllDonors(donor_hydrogen_list, PDB_file):
    donor_acceptor_pairs = []

    for donor_hydrogen_pair in donor_hydrogen_list:
        donor_atom = donor_hydrogen_pair[0]
        
        donor_x_coord, donor_y_coord, donor_z_coord = donor_atom.get_coord()

        #Lets adjust the coordinates to the Grid
        donor_x_coord = adjust_x_coord_to_Grid(donor_x_coord)
        donor_y_coord = adjust_y_coord_to_Grid(donor_y_coord)
        donor_z_coord = adjust_z_coord_to_Grid(donor_z_coord)

        #Initializing variables
        max_x_coord_forRange = 0.0
        min_x_coord_forRange = 0.0

        max_y_coord_forRange = 0.0
        min_y_coord_forRange = 0.0

        max_z_coord_forRange = 0.0
        min_z_coord_forRange = 0.0

        #First, let go forward and backward in x-direction
        max_x_coord_forRange = donor_x_coord + MAX_DONOR_ACCEPTOR_DIST
        min_x_coord_forRange = donor_x_coord - MAX_DONOR_ACCEPTOR_DIST

        #max_x_coord_forRange = doubleCheck_x_boundaries(max_x_coord_forRange)
        #min_x_coord_forRange = doubleCheck_x_boundaries(min_x_coord_forRange)

        max_x_block_forRange = int(max_x_coord_forRange // DESIRED_BOX_DIMENSTION)
        min_x_block_forRange = int(min_x_coord_forRange // DESIRED_BOX_DIMENSTION)

        max_x_block_forRange = doubleCheck_x_BoxBoundaries_General(max_x_block_forRange, xBoxDim)
        min_x_block_forRange = doubleCheck_x_BoxBoundaries_General(min_x_block_forRange, xBoxDim)


        #Next, lets go forward and backward in y-direction
        max_y_coord_forRange = donor_y_coord + MAX_DONOR_ACCEPTOR_DIST
        min_y_coord_forRange = donor_y_coord - MAX_DONOR_ACCEPTOR_DIST

        #max_y_coord_forRange = doubleCheck_y_boundaries(max_y_coord_forRange)
        #min_y_coord_forRange = doubleCheck_y_boundaries(min_y_coord_forRange)

        max_y_block_forRange = int(max_y_coord_forRange // DESIRED_BOX_DIMENSTION)
        min_y_block_forRange = int(min_y_coord_forRange // DESIRED_BOX_DIMENSTION)

        max_y_block_forRange = doubleCheck_y_BoxBoundaries_General(max_y_block_forRange, yBoxDim)
        min_y_block_forRange = doubleCheck_y_BoxBoundaries_General(min_y_block_forRange, yBoxDim)

        #Nexts, lets go forward and backward in z-direction
        max_z_coord_forRange = donor_z_coord + MAX_DONOR_ACCEPTOR_DIST
        min_z_coord_forRange = donor_z_coord - MAX_DONOR_ACCEPTOR_DIST

        #max_z_coord_forRange = doubleCheck_z_boundaries(max_z_coord_forRange)
        #min_z_coord_forRange = doubleCheck_z_boundaries(min_z_coord_forRange)

        max_z_block_forRange = int(max_z_coord_forRange // DESIRED_BOX_DIMENSTION)
        min_z_block_forRange = int(min_z_coord_forRange // DESIRED_BOX_DIMENSTION)

        max_z_block_forRange = doubleCheck_z_BoxBoundaries_General(max_z_block_forRange, zBoxDim)
        min_z_block_forRange = doubleCheck_z_BoxBoundaries_General(min_z_block_forRange, zBoxDim)

        #Add a buffer block in each direction to cover situations where atoms are exactly on the border of blocks
        max_x_block_forRange, min_x_block_forRange = add_buffer_block_in_x_direction(max_x_block_forRange, min_x_block_forRange)
        max_y_block_forRange, min_y_block_forRange = add_buffer_block_in_y_direction(max_y_block_forRange, min_y_block_forRange)
        max_z_block_forRange, min_z_block_forRange = add_buffer_block_in_z_direction(max_z_block_forRange, min_z_block_forRange)

        for x_block in range(min_x_block_forRange, max_x_block_forRange+1):
            for y_block in range(min_y_block_forRange, max_y_block_forRange+1):
                for z_block in range(min_z_block_forRange, max_z_block_forRange+1):
                    
                    grid_num = int(z_block * (xBoxDim * yBoxDim) + y_block * (xBoxDim) + x_block)

                    for acceptor_atom in grid[grid_num]:
                        donor_acceptor_pairs.append([donor_hydrogen_pair, acceptor_atom])
    return donor_acceptor_pairs

#queryBox method for random testing, method doesn't rely on any global variables
def queryBox_RandomTesting(testGrid, list_of_test_atoms, BOX_DIMENSION, lattice_dimensions, min_coordinates, max_coordinates, grid_dimensions):
    donor_acceptor_pairs = []

    #Obtaining grid dimensions and max/mins
    xDim, yDim, zDim = grid_dimensions

    min_x_coord, min_y_coord, min_z_coord = min_coordinates
    max_x_coord, max_y_coord, max_z_coord = max_coordinates

    xBoxDim, yBoxDim, zBoxDim = lattice_dimensions

    for atom in list_of_test_atoms:
        
        donor_x_coord, donor_y_coord, donor_z_coord = atom

        #Lets adjust the coordinates to the Grid
        #donor_x_coord = adjust_x_coord_to_Grid(donor_x_coord)
        #donor_y_coord = adjust_y_coord_to_Grid(donor_y_coord)
        #donor_z_coord = adjust_z_coord_to_Grid(donor_z_coord)

        #Initializing variables
        max_x_coord_forRange = 0.0
        min_x_coord_forRange = 0.0

        max_y_coord_forRange = 0.0
        min_y_coord_forRange = 0.0

        max_z_coord_forRange = 0.0
        min_z_coord_forRange = 0.0

        #First, let go forward and backward in x-direction
        max_x_coord_forRange = donor_x_coord + MAX_DONOR_ACCEPTOR_DIST
        min_x_coord_forRange = donor_x_coord - MAX_DONOR_ACCEPTOR_DIST
        #print("1. max x  =  " + str(max_x_coord_forRange) + "  min x  = " + str(min_x_coord_forRange) )

        max_x_coord_forRange = doubleCheck_x_boundaries_General(max_x_coord_forRange, xDim)
        min_x_coord_forRange = doubleCheck_x_boundaries_General(min_x_coord_forRange, xDim)
       # print("2. max x  =  " + str(max_x_coord_forRange) + "  min x  = " + str(min_x_coord_forRange) )

        max_x_block_forRange = int(max_x_coord_forRange // BOX_DIMENSION)
        min_x_block_forRange = int(min_x_coord_forRange // BOX_DIMENSION)

        #print("max_x_block = " + str(max_x_block_forRange) + "  min_x_block = " +  str(min_x_block_forRange))


        #Next, lets go forward and backward in y-direction
        max_y_coord_forRange = donor_y_coord + MAX_DONOR_ACCEPTOR_DIST
        min_y_coord_forRange = donor_y_coord - MAX_DONOR_ACCEPTOR_DIST

        max_y_coord_forRange = doubleCheck_y_boundaries_General(max_y_coord_forRange, yDim)
        min_y_coord_forRange = doubleCheck_y_boundaries_General(min_y_coord_forRange, yDim)

        max_y_block_forRange = int(max_y_coord_forRange // BOX_DIMENSION)
        min_y_block_forRange = int(min_y_coord_forRange // BOX_DIMENSION)

        #Nexts, lets go forward and backward in z-direction
        max_z_coord_forRange = donor_z_coord + MAX_DONOR_ACCEPTOR_DIST
        min_z_coord_forRange = donor_z_coord - MAX_DONOR_ACCEPTOR_DIST

        max_z_coord_forRange = doubleCheck_z_boundaries_General(max_z_coord_forRange, zDim)
        min_z_coord_forRange = doubleCheck_z_boundaries_General(min_z_coord_forRange, zDim)

        max_z_block_forRange = int(max_z_coord_forRange // BOX_DIMENSION)
        min_z_block_forRange = int(min_z_coord_forRange // BOX_DIMENSION)

        #Add a buffer block in each direction to cover situations where atoms are exactly on the border of blocks
        max_x_block_forRange, min_x_block_forRange = add_buffer_block_in_x_direction_DIFFERENT_DIMENSIONS(max_x_block_forRange, min_x_block_forRange, xBoxDim)
        max_y_block_forRange, min_y_block_forRange = add_buffer_block_in_y_direction_DIFFERENT_DIMENSIONS(max_y_block_forRange, min_y_block_forRange, yBoxDim)
        max_z_block_forRange, min_z_block_forRange = add_buffer_block_in_z_direction_DIFFERENT_DIMENSIONS(max_z_block_forRange, min_z_block_forRange, zBoxDim)

       # print(atom)
        #print("donor_x = " + str(donor_x_coord) + "  donor y = " + str(donor_y_coord) +  " donor z = " + str(donor_z_coord))
       # print("max x = " +  str(max_x_block_forRange) + "  min x = " + str(min_x_block_forRange))
        #print("max y = " +  str(max_y_block_forRange) + "  min y = " + str(min_y_block_forRange))
        #print("max z = " +  str(max_z_block_forRange) + "  min z = " + str(min_z_block_forRange))

        for x_block in  range(min_x_block_forRange, max_x_block_forRange+1):
            for y_block in range(min_y_block_forRange, max_y_block_forRange+1):
                for z_block in range(min_z_block_forRange, max_z_block_forRange+1):
                    
                    grid_num = int(z_block * (xBoxDim * yBoxDim) + y_block * (xBoxDim) + x_block)
                    #print("x block = " + str(x_block) + "    xBoxDim = " + str(xBoxDim))
                    #print("y block = " + str(y_block) + "    yBoxDim = " + str(yBoxDim))
                    #print("z block = " + str(z_block) + "    zBoxDim = " + str(zBoxDim))
                    #print(grid_num)
                    for acceptor_atom in testGrid[grid_num]:
                        donor_acceptor_pairs.append([atom, acceptor_atom])
    return donor_acceptor_pairs   

#queryBox method for General Cases, method doesn't rely on any global variables
def queryBox_DifferentSizes(testGrid, list_of_donor_atoms, BOX_DIMENSION, lattice_dimensions, min_coordinates, gridDimensions):
    donor_acceptor_pairs = []

    xBoxDim, yBoxDim, zBoxDim = lattice_dimensions
    min_x_coordinate, min_y_coordinate, min_z_coordinate = min_coordinates
    xdimension, ydimension, zdimension = gridDimensions

    for donor_hydrogen_pair in list_of_donor_atoms:
        donor_atom = donor_hydrogen_pair[0]
        
        donor_x_coord, donor_y_coord, donor_z_coord = donor_atom.get_coord()

        #Lets adjust the coordinates to the Grid
        donor_x_coord = adjust_x_coord_to_Grid_General(donor_x_coord, min_x_coordinate)
        donor_y_coord = adjust_y_coord_to_Grid_General(donor_y_coord, min_y_coordinate)
        donor_z_coord = adjust_z_coord_to_Grid_General(donor_z_coord, min_z_coordinate)

        #Initializing variables
        max_x_coord_forRange = 0.0
        min_x_coord_forRange = 0.0

        max_y_coord_forRange = 0.0
        min_y_coord_forRange = 0.0

        max_z_coord_forRange = 0.0
        min_z_coord_forRange = 0.0

        #First, let go forward and backward in x-direction
        max_x_coord_forRange = donor_x_coord + MAX_DONOR_ACCEPTOR_DIST
        min_x_coord_forRange = donor_x_coord - MAX_DONOR_ACCEPTOR_DIST
   
        max_x_block_forRange = int(max_x_coord_forRange // BOX_DIMENSION)        
        min_x_block_forRange = int(min_x_coord_forRange // BOX_DIMENSION)

        max_x_block_forRange = doubleCheck_x_BoxBoundaries_General(max_x_block_forRange, xBoxDim)
        min_x_block_forRange = doubleCheck_x_BoxBoundaries_General(min_x_block_forRange, xBoxDim)

        #Next, lets go forward and backward in y-direction
        max_y_coord_forRange = donor_y_coord + MAX_DONOR_ACCEPTOR_DIST
        min_y_coord_forRange = donor_y_coord - MAX_DONOR_ACCEPTOR_DIST

        max_y_block_forRange = int(max_y_coord_forRange // BOX_DIMENSION)
        min_y_block_forRange = int(min_y_coord_forRange // BOX_DIMENSION)

        max_y_block_forRange = doubleCheck_y_BoxBoundaries_General(max_y_block_forRange, yBoxDim)
        min_y_block_forRange = doubleCheck_y_BoxBoundaries_General(min_y_block_forRange, yBoxDim)

        #Nexts, lets go forward and backward in z-direction
        max_z_coord_forRange = donor_z_coord + MAX_DONOR_ACCEPTOR_DIST
        min_z_coord_forRange = donor_z_coord - MAX_DONOR_ACCEPTOR_DIST

        max_z_block_forRange = int(max_z_coord_forRange // BOX_DIMENSION)
        min_z_block_forRange = int(min_z_coord_forRange // BOX_DIMENSION)

        max_z_block_forRange = doubleCheck_z_BoxBoundaries_General(max_z_block_forRange, zBoxDim)
        min_z_block_forRange = doubleCheck_z_BoxBoundaries_General(min_z_block_forRange, zBoxDim)

        #Add a buffer block in each direction to cover situations where atoms are exactly on the border of blocks
        max_x_block_forRange, min_x_block_forRange = add_buffer_block_in_x_direction_DIFFERENT_DIMENSIONS(max_x_block_forRange, min_x_block_forRange, xBoxDim)
        max_y_block_forRange, min_y_block_forRange = add_buffer_block_in_y_direction_DIFFERENT_DIMENSIONS(max_y_block_forRange, min_y_block_forRange, yBoxDim)
        max_z_block_forRange, min_z_block_forRange = add_buffer_block_in_z_direction_DIFFERENT_DIMENSIONS(max_z_block_forRange, min_z_block_forRange, zBoxDim)

        #Iterates through the sub-box in lattice and finds all possible acceptors
        for x_block in  range(min_x_block_forRange, max_x_block_forRange+1):
            for y_block in range(min_y_block_forRange, max_y_block_forRange+1):
                for z_block in range(min_z_block_forRange, max_z_block_forRange+1):
                    
                    grid_num = int(z_block * (xBoxDim * yBoxDim) + y_block * (xBoxDim) + x_block)

                    for acceptor_atom in testGrid[grid_num]:
                        donor_acceptor_pairs.append([donor_hydrogen_pair, acceptor_atom])
    return donor_acceptor_pairs  

#Will return the antecedent atom to an acceptor
def getAcceptorAntecedent(acceptor_atom):
    parent_residue = acceptor_atom.get_parent()
    parent_resname = parent_residue.get_resname()

    acceptor_name = acceptor_atom.get_name()

    acceptor_donor_dictionary = get_acceptor_donor_dictionary()

    #Get the acceptor number
    acceptor_num = -1
    for key in acceptor_donor_dictionary[parent_resname]:
        if key[0] == "A" and key[1] != "A" and acceptor_donor_dictionary[parent_resname][key] == acceptor_name:
            acceptor_num = key[1]

    #Get the acceptor antecedent name
    acceptor_antecedent_name = acceptor_donor_dictionary[parent_resname]["AA" + acceptor_num]

    #Get the acceptor antecedent atom
    acceptor_antecedent_found = -1
    for atom in parent_residue:
        if atom.get_name() == acceptor_antecedent_name:
            acceptor_antecedent_atom = atom
            acceptor_antecedent_found = 1
    
    if acceptor_antecedent_found < 0:
        for atom in parent_residue: #Randomly assign an atom
            acceptor_antecedent_atom = atom

    return [acceptor_antecedent_atom, acceptor_antecedent_found]

#Will go through list of potential H-Bonds and filter out H-Bonds
#that don't fit the geometric criteria
def filterListOfPotentialHBonds(potential_H_bonds):
    final_list_of_H_Bonds = []
    count = 0

    #Iteratively will check each potential hydrogen bond
    for pair in potential_H_bonds:
        notValidBond = 0

        #Extracts Biopython Atom objects and stores in variables
        donor_atom = pair[0][0]
        acceptor_atom = pair[1]
        hydrogen_atom = pair[0][1]

        #Appends warnings if either donor or acceptor atom is disordered (indicated by label in PDB file)
        if donor_atom.is_disordered() != 0:
            warnings_list.append("WARNING: " + donor_atom.get_name() + " in " +  donor_atom.get_parent().get_resname() + " is a disordered atom. Could lead to incorrect hydrogen bonds.")
        if acceptor_atom.is_disordered() != 0:
            warnings_list.append("WARNING: " + acceptor_atom.get_name() + " in " +  acceptor_atom.get_parent().get_resname() + " is a disordered atom. Could lead to incorrect hydrogen bonds.")
      
        donor_residue_id = donor_atom.get_parent().get_id()
        donor_hetfield = donor_residue_id[0]

        #D-A max distance of 3.9 Angstroms
        x2, y2, z2 = donor_atom.get_coord()
        x1, y1, z1 = acceptor_atom.get_coord()

        #x2, y2, z2 are for donor / x1, y1, z1 are for acceptor
        dist_between_donor_acceptor = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)

        #Checks if donor is water molecule, because certain checks won't apply (hetfield is an attribute of a Biopython residue)
        #All checks that involve using an hydrogen position from input, will NOT be checked.

        #The number of hydrogen bonds is not explicit counted, so a water molecule could be recorded to form more than 2 hydrogen bonds. 
        #REMEMBER: the goal of the software is to find all the plausible hydrogen bonds to could form, not to find one set of hydrogen bonds 
        #is mostly likely to occur
        if donor_hetfield != "W":

            #H-A max distance of 2.5
            x2, y2, z2 = hydrogen_atom.get_coord()
            x1, y1, z1 = acceptor_atom.get_coord()
            dist_between_hydrogen_acceptor = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)

            #Makes sure H-A is an approriate distance (raises flag if doesn't match criteria)
            if dist_between_hydrogen_acceptor > 2.5:
                notValidBond = 1

            #D-H-A min angle of 90
            donor_vector = donor_atom.get_vector()
            hydrogen_vector = hydrogen_atom.get_vector()
            acceptor_vector = acceptor_atom.get_vector()
            D_H_A_angle = calc_angle(donor_vector, hydrogen_vector, acceptor_vector)
            D_H_A_angle = math.degrees(D_H_A_angle)

            #Angle checks between donor, hydrogen, acceptor & acceptor antecedents
            if D_H_A_angle < 90:
                notValidBond = 1
        else:
            #hydrogens in waters are assumed to be 1 Angstrom from Donor, in line between donor and acceptor
            if dist_between_donor_acceptor > 3.50:
                notValidBond = 1

        acceptor_residue_id = acceptor_atom.get_parent().get_id()
        acceptor_hetfield = acceptor_residue_id[0]
        
        #Does not perform these checks on acceptors from water molecules since there are no acceptor antecedent
        if acceptor_hetfield != "W":
            acceptor_antecedent_atom, found_status = getAcceptorAntecedent(acceptor_atom)
        
            #Checks that the D-A-AA angle >= 90
            if found_status > 0:
                donor_vector = donor_atom.get_vector()
                acceptor_vector = acceptor_atom.get_vector()
                acceptor_antecedent_vector = acceptor_antecedent_atom.get_vector()
                D_A_AA_angle = calc_angle(donor_vector, acceptor_vector, acceptor_antecedent_vector)
                D_A_AA_angle = math.degrees(D_A_AA_angle)
            else:
                D_A_AA_angle = -1

            #Checks that the H-A-AA angle >= 90
            if found_status > 0:
                hydrogen_vector = hydrogen_atom.get_vector()
                acceptor_vector = acceptor_atom.get_vector()
                acceptor_antecedent_vector = acceptor_antecedent_atom.get_vector()
                H_A_AA_angle = calc_angle(hydrogen_vector, acceptor_vector, acceptor_antecedent_vector)
                H_A_AA_angle = math.degrees(H_A_AA_angle)      
            else:
                H_A_AA_angle = -1

            if D_A_AA_angle < 90:
                notValidBond = 1
            if H_A_AA_angle < 90:
                notValidBond = 1

        #Makes sure the H-Bond isn't between the same atom
        if donor_atom.get_full_id() == acceptor_atom.get_full_id():
            notValidBond = 1

        #Makes sure it is within the approriate distance
        if dist_between_donor_acceptor > 3.90:
            notValidBond = 1

        #Adds in the H-Bond if it satisfies all the previous tests
        if notValidBond == 0:
            final_list_of_H_Bonds.append(pair)

    return final_list_of_H_Bonds

#Returns the distance and angle information for each hydrogen bond
def getHBondInformation(listOfHBonds):
    #Each H-Bond will have a list element in final list with the following order
    #[D-A, H-A, D-H-A, D-A-AA, H-A-AA]
    final_list_of_H_Bonds = []
    count = 0

    for pair in listOfHBonds:
        notValidBond = 0
        currentHBond = []

        donor_atom = pair[0][0]
        acceptor_atom = pair[1]
        hydrogen_atom = pair[0][1]
        
        donor_residue_id = donor_atom.get_parent().get_id()
        donor_hetfield = donor_residue_id[0]

        #D-A max distance of 3.9
        x2, y2, z2 = donor_atom.get_coord()
        x1, y1, z1 = acceptor_atom.get_coord()
        dist_between_donor_acceptor = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)
        currentHBond.append(dist_between_donor_acceptor)

        #checks if donor is a oxygen from a water molecule, since there will be no hydrogen atom
        if donor_hetfield != "W":
            #H-A max distance of 2.5
            x2, y2, z2 = hydrogen_atom.get_coord()
            x1, y1, z1 = acceptor_atom.get_coord()
            dist_between_hydrogen_acceptor = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)
            currentHBond.append(dist_between_hydrogen_acceptor)

            #D-H-A min angle of 90
            donor_vector = donor_atom.get_vector()
            hydrogen_vector = hydrogen_atom.get_vector()
            acceptor_vector = acceptor_atom.get_vector()
            D_H_A_angle = calc_angle(donor_vector, hydrogen_vector, acceptor_vector)
            D_H_A_angle = math.degrees(D_H_A_angle)

            currentHBond.append(D_H_A_angle)
        else:
            #HBPlus defines a hydrogen for a water 1 angstrom away from oxygen
            dist_between_hydrogen_acceptor = dist_between_donor_acceptor - 1.0
            currentHBond.append(dist_between_hydrogen_acceptor)
            D_H_A_angle = -1.0
            currentHBond.append(D_H_A_angle)

        acceptor_residue_id = acceptor_atom.get_parent().get_id()
        acceptor_hetfield = acceptor_residue_id[0]
        
        #Does not perform these checks on acceptors from water molecules since there are no AA
        if acceptor_hetfield != "W":
            acceptor_antecedent_atom, founds_status = getAcceptorAntecedent(acceptor_atom)
        
            #D-A-AA min angle of 90
            if founds_status > 0:
                donor_vector = donor_atom.get_vector()
                acceptor_vector = acceptor_atom.get_vector()
                acceptor_antecedent_vector = acceptor_antecedent_atom.get_vector()
                D_A_AA_angle = calc_angle(donor_vector, acceptor_vector, acceptor_antecedent_vector)
                D_A_AA_angle = math.degrees(D_A_AA_angle)
            else:
                D_A_AA_angle = -1

            currentHBond.append(D_A_AA_angle)

            #H-A-AA min angle of 90
            if founds_status > 0:
                hydrogen_vector = hydrogen_atom.get_vector()
                acceptor_vector = acceptor_atom.get_vector()
                acceptor_antecedent_vector = acceptor_antecedent_atom.get_vector()
                H_A_AA_angle = calc_angle(hydrogen_vector, acceptor_vector, acceptor_antecedent_vector)
                H_A_AA_angle = math.degrees(H_A_AA_angle)  
            else:
                H_A_AA_angle = -1
                
            currentHBond.append(H_A_AA_angle)    
        else:
            
            D_A_AA_angle = -1.0
            currentHBond.append(D_A_AA_angle)

            H_A_AA_angle = -1.0
            currentHBond.append(H_A_AA_angle)

        #Adds information list to final list
        final_list_of_H_Bonds.append(currentHBond)

    return final_list_of_H_Bonds  

#Filter method for the random testing function
def filterListOfPotentialHBonds_RandomTesting(potential_H_bonds):
    final_list_of_H_Bonds = []
    count = 0

    for pair in potential_H_bonds:
        donor_atom = pair[0]
        acceptor_atom = pair[1]

        x2, y2, z2 = donor_atom
        x1, y1, z1 = acceptor_atom
        dist_between_donor_acceptor = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)

        notValidBond = 0

        #Makes sure it is within the approriate distance
        if dist_between_donor_acceptor > 3.90:
            notValidBond = 1
        #Adds in the H-Bond if it satisfies all the previous tests
        if notValidBond == 0:
            final_list_of_H_Bonds.append(pair)
    return final_list_of_H_Bonds

#Get the max and min coordinates of a pdbfile in each direction
def getMaxAndMinCoordinates(pdb_file):
    structure = parser.get_structure("structure_id", pdb_file)
    max_x_coord = -sys.maxsize-1
    max_y_coord = -sys.maxsize-1
    max_z_coord =  -sys.maxsize-1

    min_x_coord = sys.maxsize
    min_y_coord = sys.maxsize
    min_z_coord = sys.maxsize

    #Obtaining the max and min coordinates in each dimension
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    x_coord, y_coord, z_coord = atom.get_coord()
                    if x_coord > max_x_coord:
                        max_x_coord = x_coord
                    if x_coord < min_x_coord: 
                        min_x_coord = x_coord

                    if y_coord > max_y_coord:
                        max_y_coord = y_coord
                    if y_coord < min_y_coord: 
                        min_y_coord = y_coord

                    if z_coord > max_z_coord:
                        max_z_coord = z_coord
                    if z_coord < min_z_coord:
                        min_z_coord = z_coord
    max_coordinates = [max_x_coord, max_y_coord, max_z_coord]
    min_coordinates = [min_x_coord, min_y_coord, min_z_coord]
    return ([max_coordinates, min_coordinates])

#Return the length of the lattice in each direction
def calculateDimensions(max_coordinates, min_coordinates):
    max_x_coord, max_y_coord, max_z_coord = max_coordinates
    min_x_coord, min_y_coord, min_z_coord = min_coordinates

    xdim = max_x_coord - min_x_coord + 2
    ydim = max_y_coord - min_y_coord + 2
    zdim = max_z_coord - min_z_coord + 2

    return [xdim, ydim, zdim]

#Returns the average atom density of the lattice
def getAverageDensityOfLattice(grid):
    total_num_atoms = 0
    total_num_boxes = 0
    for box in grid:
        total_num_atoms = total_num_atoms + len(box)
        total_num_boxes = total_num_boxes + 1
    #print("total boxes = " +  str(total_num_boxes) + "   total atoms = " + str(total_num_atoms))
    return (total_num_atoms/total_num_boxes)


def printHBonds_Table(listOfHBonds, listOfHBondInformation, PDB_File):
    #Gets the PDB Code and opens file to write to
    file_name_split = (PDB_File.split("/"))
    PDB_code = file_name_split[len(file_name_split)-1]

    PDB_code_str = (PDB_code.split("."))[0]
    file_name = "HBondFinder_" + PDB_code_str + ".txt"
    print("Writing to " + str(file_name) + " ...")

    f = open(file_name, "w+")
    f.write("<------ DONOR ------><---- ACCEPTOR --------->     D-A    H-A    D-H-A    D-A-AA   H-A-AA\n")
    count = 0

    hbondReport = open("hbonds_" + PDB_code_str + ".txt", "w+")
    listOfAtoms = []
    num_of_atoms = 0
    num_of_hbonds = 0
    
    #Iterates through all the hydrogen bonds
    for HBond in listOfHBonds:
        Donor_Hydrogen_Pair, acceptor_atom = HBond
        donor_atom = Donor_Hydrogen_Pair[0]

        currentBondInfo = listOfHBondInformation[count]

        #Print the Donor, and then Acceptor Information
        donor_resname = donor_atom.get_parent().get_resname()
        donor_structure_id, donor_model_num, donor_chain_name, donor_residue_info, donor_atom_info = donor_atom.get_full_id()
        
        #Getting the Residue Number
        str_One, donor_residue_num, str_Two = donor_residue_info

        #Getting the Atom Name
        donor_atom_name, str_Two = donor_atom_info

        #Now, lets get the Acceptor Info
        acceptor_resname = acceptor_atom.get_parent().get_resname()
        acceptor_structure_id, acceptor_model_num, acceptor_chain_name, acceptor_residue_info, acceptor_atom_info = acceptor_atom.get_full_id()

        #Getting the Residue Number
        str_One, acceptor_residue_num, str_Two = acceptor_residue_info

        #Getting the Atom Name
        acceptor_atom_name, str_Two = acceptor_atom_info

        f.write(str(donor_chain_name).ljust(4) + str(donor_residue_num).ljust(7) + str(donor_resname).ljust(7) + str(donor_atom_name).ljust(7) + str(acceptor_chain_name).ljust(5) +str(acceptor_residue_num).ljust(7) + str(acceptor_resname).ljust(7)
        + str(acceptor_atom_name).ljust(7) + str("{0:.2f}".format(currentBondInfo[0])).ljust(7) + str("{0:.2f}".format(currentBondInfo[1])).ljust(7) + str("{0:.2f}".format(currentBondInfo[2])).ljust(9) + 
        str("{0:.2f}".format(currentBondInfo[3])).ljust(9) + str("{0:.2f}".format(currentBondInfo[4])).ljust(9)+ "\n")
        count = count + 1

        #Will add atom to list of atoms if not already in it
        if donor_atom not in listOfAtoms:
            listOfAtoms.append(donor_atom)
        if acceptor_atom not in listOfAtoms:
            listOfAtoms.append(acceptor_atom)

        #f.write(str(donor_resname) + "  " + str(donor_residue_num) + "  " + str(donor_atom_name) + "     " + str(acceptor_resname) + "  " + str(acceptor_residue_num) + "  " + str(acceptor_atom_name) + "\n")
    f.close()

    #Iterates through hydrogen bonds and write input file for graph neural network
    hbondReport.write("#NUMBER_OF_ATOMS " + str(len(listOfAtoms)) + "\n")
    index = 0
    for atom in listOfAtoms:
        structure_id, model_num, chain_name, residue_info, atom_info  = atom.get_full_id()

        #Extract key info to print in file
        str_One, residue_num, str_Two = residue_info
        atom_resname = atom.get_parent().get_resname()
        atom_name = atom.get_id()
        x_coord, y_coord, z_coord = atom.get_coord()
        atom_serialNum = atom.get_serial_number()

        hbondReport.write(str(chain_name).ljust(5) + str(atom_resname).ljust(5) + str(residue_num).ljust(7) + str(atom_name).ljust(5) + str(index).ljust(5) + str(x_coord).ljust(9) + str(y_coord).ljust(9) + str(z_coord).ljust(9) + str(atom_serialNum).ljust(7) + "\n")
        index = index  + 1
    
    #List all hydrogen bonds to file
    hbondReport.write("#NUMBER_OF_HBONDS " + str(len(listOfHBonds)) + "\n")  
    for HBond in listOfHBonds:
        Donor_Hydrogen_Pair, acceptor_atom = HBond
        donor_atom = Donor_Hydrogen_Pair[0]

        donor_index = listOfAtoms.index(donor_atom)
        acceptor_index = listOfAtoms.index(acceptor_atom)

        hbondReport.write(str(donor_index).ljust(6) + str(acceptor_index).ljust(6) + "\n")
    hbondReport.close()




def usageMethod():
    print("\nHBondFinder Software: Version 1.0")
    print("Description: Finds all possible hydrogen bonds in PDB File.")
    print("Usage: python hbondfinder.py [OPTIONS]")
    print("Options:")
    print("         -h, --help")
    print("                 Prints usage message for this program and various options.")
    print("         -i FILE, --input FILE")
    print("                 File with atomic coordinates (should already include hydrogen positions)")  
    print("         -w, --warning")
    print("                 Prints out all warnings encountered during program execution.") 
    print("         -j FILE, --json FILE")
    print("                 JSON file that encodes the naming scheme for hydrogens.") 
    print("         -d double, --dimension double")
    print("                 Box dimension used for building lattice structure (Default is 4.0 A)")
    print("         -b batching_dir_str, --batchingDir batching_dir_str")
    print("                 Allows user to specify directory containing PDB files to be run through program.")
#End of Helper Methods ---------------------------------------------------

 

#Unit Test Methods and Optimization Methods ------------------------------

#Does an exhaustive search of the lattice for each donor atom, to see if
#queryBox has correctly identified all the potential H-Bonds
def queryBox_UnitTest1(listOfHBonds, donor_hydrogen_list, lattice_dimensions):
    xBoxDimension, yBoxDimension, zBoxDimension = lattice_dimensions
    H_Bond_List = []
    for donor_pair in donor_hydrogen_list:
        donor_atom = donor_pair[0]

        #Goes through every single block in lattice
        for i in range(xBoxDimension*yBoxDimension*zBoxDimension):
            for acceptor_atom in grid[i]:
                #Gets coordinates and calculates distance
                x2, y2, z2 = donor_atom.get_coord()
                x1, y1, z1 = acceptor_atom.get_coord()
                distance = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 ) ** (1.0/2.0)

                if distance <= 3.90 and distance > 0:
                    H_Bond_List.append([donor_pair, acceptor_atom])

    #Makes sure both lists are subsets of each other, proving equality
    return (all(elem in H_Bond_List for elem in listOfHBonds) and all(elem in listOfHBonds for elem in H_Bond_List)) 

#Goes through each box in lattice and makes sure that each atom in there
#should be there
def buildGrid_UnitTest1(grid, lattice_dimensions, min_coordinates):
    xBoxDimension, yBoxDimension, zBoxDimension = lattice_dimensions
    x_min_coord, y_min_coord, z_min_coord = min_coordinates

    notValid = False
    for x in range(xBoxDimension):
        for y in range(yBoxDimension):
            for z in range(zBoxDimension):
                for j in grid[int(z * (xBoxDim * yBoxDim) + y * (xBoxDim) + x)]:
                    x_coord, y_coord, z_coord = j.get_coord()

                    #Now turn all coordinates to positive values by adding the minus value of dimension
                    x_coord_pos = adjust_x_coord_to_Grid_General(x_coord, x_min_coord)
                    y_coord_pos = adjust_y_coord_to_Grid_General(y_coord, y_min_coord)
                    z_coord_pos = adjust_z_coord_to_Grid_General(z_coord, z_min_coord)

                    #Check that the coordinates are within the correct range
                    if x_coord_pos < (x * BOX_DIMENSION) or x_coord_pos > ((x+1) * BOX_DIMENSION):
                        notValid = True
                
                    if y_coord_pos < (y * BOX_DIMENSION) or y_coord_pos > ((y+1) * BOX_DIMENSION):
                        notValid = True

                    if z_coord_pos < (z * BOX_DIMENSION) or z_coord_pos > ((z+1) * BOX_DIMENSION):
                        notValid = True
    return notValid


def randomizedTestingForBuildGrid_queryBox():


    #Setting up the min and max coordinates in each direction
    min_x_coord = 0
    min_y_coord = 0
    min_z_coord = 0
    minimum_coords = [min_x_coord, min_y_coord, min_z_coord]

    max_x_coord = 100
    max_y_coord = 100
    max_z_coord = 100
    maximum_coords = [max_x_coord, max_y_coord, max_z_coord]

    #Calculating dimensions of the grid
    xDim, yDim, zDim = calculateDimensions(maximum_coords, minimum_coords)
    grid_dimensions = [xDim, yDim, zDim]
    
    #Randomly generate coordinates to put into lattice
    list_of_coords = []
    for i in range(100):
        x = random.uniform(min_x_coord, max_x_coord)
        y = random.uniform(min_y_coord, max_y_coord)
        z = random.uniform(min_z_coord, max_z_coord)
        list_of_coords.append([x,y,z])

    #Randomly generate atoms to query on
    list_of_test_atoms = []
    for i in range(100):
        x = random.uniform(min_x_coord, max_x_coord)
        y = random.uniform(min_y_coord, max_y_coord)
        z = random.uniform(min_z_coord, max_z_coord)
        list_of_test_atoms.append([x,y,z])
    
    # Workbook is created 
    wb = Workbook() 
  
    #add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 
    




    list_Of_Box_Dimensions = [30.0, 20.0, 15.0, 10.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.50]
    count = 0

    for box_dimension in list_Of_Box_Dimensions:

        #Setting up a small box
        xBoxDimension = getBoxDimension_DifferentDimensions(xDim, box_dimension)
        yBoxDimension = getBoxDimension_DifferentDimensions(yDim, box_dimension)
        zBoxDimension = getBoxDimension_DifferentDimensions(zDim, box_dimension)
        lattice_dimensions = [xBoxDimension, yBoxDimension, zBoxDimension]
       # print(lattice_dimensions)
        start = time.time()
        #Build Lattice of Coordinates
        testGrid = grid = [[] for i in range(int(xBoxDimension * yBoxDimension * zBoxDimension))]
        testGrid = buildGrid_RandomTesting(list_of_coords, testGrid, box_dimension, lattice_dimensions)
    
    
        #Now lets query
        potentialHBonds = queryBox_RandomTesting(testGrid, list_of_test_atoms, box_dimension, lattice_dimensions, minimum_coords, maximum_coords, grid_dimensions)
        HBondsList = filterListOfPotentialHBonds_RandomTesting(potentialHBonds)
        #print(len(HBondsList))
        end = time.time()

        atom_density = getAverageDensityOfLattice(testGrid)

        #Print result
        print("Dimension:  " +  str(box_dimension)  + "  Time Elapsed: " + str(end - start) + "  Atom Density = " + str(atom_density))
        sheet1.write(count, 0, box_dimension)
        sheet1.write(count, 1, (end-start))
        sheet1.write(count, 2, atom_density)
        count = count + 1
        #Now lets manually test every possible atom in lattice, and see if we
        #get the same list
        #final_list = []
        #for atom1 in list_of_test_atoms:
         #   for i in range(xBoxDim*yBoxDim*zBoxDim):
          #      for atom2 in testGrid[i]:
           #         x2, y2, z2 = atom2
            #        x1, y1, z1 = atom1

             #       distance = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)
              #      if distance <= 3.90:
               #         final_list.append([atom1, atom2])
                
        #print(len(final_list))
    wb.save('1hundred_grid_100_query_4.xls')
    #return (all(elem in final_list for elem in HBondsList) and all(elem in HBondsList for elem in final_list))
   
def specificTestingForBuildGrid_queryBox():
    #Specifically, generate coordinates to put into lattice
    list_of_coords = [[0.0, 4.0, 0.0]]
    #Build Lattice of Coordinates
    testGrid = grid = [[] for i in range(int(xBoxDim * yBoxDim * zBoxDim))]
    testGrid = buildGrid_RandomTesting(list_of_coords, testGrid)

    #Randomly generate atoms to query on
    list_of_test_atoms = [[0.0, 8.0, 0.0], [40.0, 40.0, 40.0]]

    #Now lets query
    potentialHBonds = queryBox_RandomTesting(testGrid, list_of_test_atoms)
    HBondsList = filterListOfPotentialHBonds_RandomTesting(potentialHBonds)

    #Now lets manually test every possible atom in lattice, and see if we
    #get the same list
    final_list = []
    for atom1 in list_of_test_atoms:
        for i in range(xBoxDim*yBoxDim*zBoxDim):
            for atom2 in testGrid[i]:
                x2, y2, z2 = atom2
                x1, y1, z1 = atom1

                distance = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2 )**(1.0/2.0)
                if distance <= 3.90:
                    final_list.append([atom1, atom2])
    #print(len(HBondsList))
    #print(len(final_list))

    return (all(elem in final_list for elem in HBondsList) and all(elem in HBondsList for elem in final_list))  

def testingSingleBoxSize(PDB_File, BOX_DIMENSION):
        #Get the max and min coordinates in each direction
        max_min_coordinates = getMaxAndMinCoordinates(PDB_File)
        max_coordinates = max_min_coordinates[0]
        min_coordinates = max_min_coordinates[1]
        max_x_coord, max_y_coord, max_z_coord = max_coordinates
        min_x_coord, min_y_coord, min_z_coord = min_coordinates

        #Calculate the dimensions in each direction
        xdim, ydim, zdim = calculateDimensions(max_coordinates, min_coordinates)
        gridDimensions = [xdim, ydim, zdim]
        
        #Calculating the box dimension
        xBoxDim = getBoxDimension_DifferentDimensions(xdim, BOX_DIMENSION)
        yBoxDim = getBoxDimension_DifferentDimensions(ydim, BOX_DIMENSION)
        zBoxDim = getBoxDimension_DifferentDimensions(zdim, BOX_DIMENSION)
        lattice_dimensions = [xBoxDim, yBoxDim, zBoxDim]
        
        #Get a list of acceptor atoms and donor/hydrogen pairs
        acceptor_list = getListOfAcceptorAtoms(PDB_File)
        donor_hydrogen_list = getListOfDonorAndHydrogenAtoms(PDB_File)

        donor_hydrogen_list = addDonorOxygenFromWaters(PDB_File, donor_hydrogen_list)
        
        #Create an list of lists that represents a 3D-lattice of the protein
        testGrid = [[] for i in range(int(xBoxDim * yBoxDim * zBoxDim))]

        start = time.time()
        #Builds the Lattice with the acceptor atoms and querys on all donor atoms
        testGrid = buildGrid_DifferentSizes(acceptor_list, testGrid, BOX_DIMENSION, lattice_dimensions, min_coordinates)
        listOfPotentialHBonds = queryBox_DifferentSizes(testGrid, donor_hydrogen_list, BOX_DIMENSION, lattice_dimensions, min_coordinates, gridDimensions)
        end = time.time()

        #Filters out H-Bonds that don't follow specific geometric criteria
        listOfHBonds = filterListOfPotentialHBonds(listOfPotentialHBonds)
        HBond_Information = getHBondInformation(listOfHBonds)
        printHBonds_Table(listOfHBonds, HBond_Information, PDB_File)

        print(str(len(listOfHBonds)) + " Hydrogen Bonds were found.")

def testingDifferentBoxSizes(PDB_File, count):
    list_Of_Dimensions = [30,25,20,15,10,5,3,2,1]

    sheet1.write(count, 0, PDB_File)
    for i in range(len(list_Of_Dimensions)):
        #print("Dimensions: " + str(list_Of_Dimensions[i]))
        #Get the max and min coordinates in each direction
        max_min_coordinates = getMaxAndMinCoordinates(PDB_File)
        max_coordinates = max_min_coordinates[0]
        min_coordinates = max_min_coordinates[1]
        max_x_coord, max_y_coord, max_z_coord = max_coordinates
        min_x_coord, min_y_coord, min_z_coord = min_coordinates

        #print("Max-Coordinates: " + str(max_coordinates))
        #print("Min-Coordinates: " + str(min_coordinates))

        #Calculate the dimensions in each direction
        xdim, ydim, zdim = calculateDimensions(max_coordinates, min_coordinates)
        gridDimensions = [xdim, ydim, zdim]
        #print(gridDimensions)
        
        #Calculating the box dimension
        BOX_DIMENSION = list_Of_Dimensions[i]
        xBoxDim = getBoxDimension_DifferentDimensions(xdim, BOX_DIMENSION)
        yBoxDim = getBoxDimension_DifferentDimensions(ydim, BOX_DIMENSION)
        zBoxDim = getBoxDimension_DifferentDimensions(zdim, BOX_DIMENSION)
        lattice_dimensions = [xBoxDim, yBoxDim, zBoxDim]
        #print(lattice_dimensions)
        
        #Get a list of acceptor atoms and donor/hydrogen pairs
        acceptor_list = getListOfAcceptorAtoms(PDB_File)
        donor_hydrogen_list = getListOfDonorAndHydrogenAtoms(PDB_File)

        #Create an list of lists that represents a 3D-lattice of the protein
        testGrid = [[] for i in range(int(xBoxDim * yBoxDim * zBoxDim))]

        start = time.time()
        #Builds the Lattice with the acceptor atoms
        testGrid = buildGrid_DifferentSizes(acceptor_list, testGrid, BOX_DIMENSION, lattice_dimensions, min_coordinates)

        listOfPotentialHBonds = queryBox_DifferentSizes(testGrid, donor_hydrogen_list, BOX_DIMENSION, lattice_dimensions, min_coordinates, gridDimensions)
        end = time.time()
        listOfHBonds = filterListOfPotentialHBonds(listOfPotentialHBonds)

        elapsed_time = (end-start) * (10000)
        sheet1.write(count, (i+1), str(elapsed_time))
        print("Dimension:  " +  str(BOX_DIMENSION)  + "  Time Elapsed: " + str(end - start))

def testingVariousPDBFiles(batching_dir, BOX_DIMENSION):
    count = 0
    pdb_files = glob(batching_dir + "*")

    for file_name in pdb_files:
        if file_name != batching_dir:
            testingSingleBoxSize(file_name, BOX_DIMENSION)

#End of Unit Test Methods ----------------------------------------------
        


#Beginning of 'Main Method' Code ---------------------------------------

#Initializes various variables
warnings.simplefilter('ignore', BiopythonWarning)
warnings.simplefilter('ignore', RuntimeWarning)
warnings_list = []

MAX_DONOR_ACCEPTOR_DIST = 3.90
parser = PDBParser(PERMISSIVE=1)

#Variables for command-line options
input_file = ""
dict_json_file = ""
show_warnings = False
box_dimension = 4.0
batching_dir = ""
batching_mode = False

#Parses the command-line options
options, remainder = getopt.getopt(sys.argv[1:], "hi:wj:d:b:", ["help", "input=", "json=", "warnings", "dimension=", "batchingDir="])
for opt, arg in options:
    if opt in ("-h", "--help"):
        usageMethod()
        exit(0)
    elif opt in ("-i", "--input"):
        input_file = arg
    elif opt in ("-w", "--warning"):
        show_warnings = True
    elif opt in ("-j", "--json"):
        dict_json_file = arg
    elif opt in ("-d", "--dimension"):
        box_dimension = float(arg)
    elif opt in ("-b", "--batchingDir"):
        batching_dir = arg
        batching_mode = True


#Exits program when not given adequate information
if input_file == "" and batching_mode == False:
    print("Error: Need an input file to operate on.")
    exit(-1)
if dict_json_file == "":
    print("Error: Need a JSON file for hydrgen names to use.")
    exit(-1)  
    
#Executes the function on input file (either single file mode or batch mode)
if batching_mode:
    testingVariousPDBFiles(batching_dir, box_dimension)
else:    
    testingSingleBoxSize(input_file, box_dimension)

#Prints warnings if asked for
if show_warnings:
    for warning in warnings_list:
        print(warning)








