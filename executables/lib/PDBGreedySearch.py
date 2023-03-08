import getopt
import math
import sys


# Checks a connected graph from all points in 1st PDB file to 2nd PDB file.
# If within dist, then append index of point to output
# This point index can be referenced using splitLines (for further parsing using other parameters) or unsplitLines (to write back to PDB format easier)
def compareDist(points1, points2, dist):
    output1 = []
    for i in range(len(points1)):
        temp = [i]
        temp.append([])
        for j in range(len(points2)):
            d1 = (points1[i][0] - points2[j][0]) ** 2
            d2 = (points1[i][1] - points2[j][1]) ** 2
            d3 = (points1[i][2] - points2[j][2]) ** 2
            d = math.sqrt(d1 + d2 + d3)
            if d < dist:
                temp[1].append(str(j))
        if temp[1]:
            output1.append(temp)
    return output1
    # return output1, output2


# Output format is the same as above but adds an extra parameter of checking if amino acids are oppositely charged AND checks for a distance of 3
def compareDistIonic(output, points1, points2, dist, splitLines_PDB1, splitLines_PDB2):
    output1 = []
    for i in range(len(output)):
        pts1_idx = int(output[i][0])
        temp_AminoAcid = splitLines_PDB1[pts1_idx][3]
        charge1 = 0
        temp = [pts1_idx]
        temp.append([])
        if (
            temp_AminoAcid == "HIS"
            or temp_AminoAcid == "ARG"
            or temp_AminoAcid == "LYS"
        ):
            if (
                "NZ" in splitLines_PDB1[pts1_idx][2]
                or "NE" in splitLines_PDB1[pts1_idx][2]
                or "ND" in splitLines_PDB1[pts1_idx][2]
                or "NH" in splitLines_PDB1[pts1_idx][2]
            ):
                charge1 = 1
        elif temp_AminoAcid == "ASP" or temp_AminoAcid == "GLU":
            if (
                "OD" in splitLines_PDB1[pts1_idx][2]
                or "OE" in splitLines_PDB1[pts1_idx][2]
            ):
                charge1 = -1
        if charge1 != 0:
            for j in range(len(output[i][1])):
                charge2 = 0
                pts2_idx = int(output[i][1][j])
                temp_AminoAcid = splitLines_PDB2[pts2_idx][3]
                if (
                    temp_AminoAcid == "HIS"
                    or temp_AminoAcid == "ARG"
                    or temp_AminoAcid == "LYS"
                ):
                    if (
                        "NZ" in splitLines_PDB2[pts2_idx][2]
                        or "NE" in splitLines_PDB2[pts2_idx][2]
                        or "ND" in splitLines_PDB2[pts2_idx][2]
                        or "NH" in splitLines_PDB2[pts2_idx][2]
                    ):
                        charge2 = 1
                elif temp_AminoAcid == "ASP" or temp_AminoAcid == "GLU":
                    if (
                        "OD" in splitLines_PDB2[pts2_idx][2]
                        or "OE" in splitLines_PDB2[pts2_idx][2]
                    ):
                        charge2 = -1
                total_charge = charge1 + charge2
                if total_charge == 0:
                    # d1 = (points1[pts1_idx][0]-points2[pts2_idx][0])**2
                    # d2 = (points1[pts1_idx][1]-points2[pts2_idx][1])**2
                    # d3 = (points1[pts1_idx][2]-points2[pts2_idx][2])**2
                    # d	=	math.sqrt(d1+d2+d3)
                    # if d < dist:
                    temp[1].append(str(pts2_idx))
        if temp[1]:
            output1.append(temp)
    return output1


def compareDistCatPi(output, points1, points2, dist, splitLines_PDB1, splitLines_PDB2):
    output1 = []
    for i in range(len(output)):
        pts1_idx = int(output[i][0])
        temp_AminoAcid = splitLines_PDB1[pts1_idx][3]
        charge1 = 0
        temp = [pts1_idx]
        temp.append([])
        if temp_AminoAcid == "ARG" or temp_AminoAcid == "LYS":
            charge1 = 1
        elif (
            temp_AminoAcid == "PHE"
            or temp_AminoAcid == "TYR"
            or temp_AminoAcid == "TRP"
        ):
            charge1 = -1
        if charge1 != 0:
            for j in range(len(output[i][1])):
                charge2 = 0
                pts2_idx = int(output[i][1][j])
                temp_AminoAcid = splitLines_PDB2[pts2_idx][3]
                if temp_AminoAcid == "ARG" or temp_AminoAcid == "LYS":
                    charge2 = 1
                elif (
                    temp_AminoAcid == "PHE"
                    or temp_AminoAcid == "TYR"
                    or temp_AminoAcid == "TRP"
                ):
                    charge2 = -1
                total_charge = charge1 + charge2
                if total_charge == 0:
                    # d1 = (points1[pts1_idx][0]-points2[pts2_idx][0])**2
                    # d2 = (points1[pts1_idx][1]-points2[pts2_idx][1])**2
                    # d3 = (points1[pts1_idx][2]-points2[pts2_idx][2])**2
                    # d	=	math.sqrt(d1+d2+d3)
                    # if d < dist:
                    temp[1].append(str(pts2_idx))
        if temp[1]:
            output1.append(temp)
    return output1
