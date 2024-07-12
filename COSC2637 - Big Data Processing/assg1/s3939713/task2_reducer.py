#!/usr/bin/env python3
"""task2_reducer.py"""

import sys
from math import sqrt

def convert_line(line):
    medoid_idx, x, y = line.split('\t')

    # convert x and y (currently a string) to float
    try:
        x = float(x)
        y = float(y)
        obj = (x, y)

        return medoid_idx, obj
    except:
        # float was not a number, so silently
        # ignore/discard this line
        return None, None

def calculateMinMedoids(lines, medoid_idx, tmp_medoid_obj, min_dist):
    # looping lines for comparing dist within medoid
    prev_inner_obj = None
    tmp_dist = 0
    for inner_line in lines:
        inner_medoid_idx, inner_obj = convert_line(inner_line)

        # read line without error
        if inner_medoid_idx is not None:

            # handle inner obj associate with same medoid only
            if medoid_idx == inner_medoid_idx:

                # calculate distance for obj diff with prev_obj only
                # as same obj has 0 distance
                if inner_obj != prev_inner_obj or prev_inner_obj is None:
                    # euclidian distance from every point of dataset
                    # to every medoid
                    cur_dist = sqrt(pow(inner_obj[0] - tmp_medoid_obj[0], 2) + pow(inner_obj[1] - tmp_medoid_obj[1], 2))
                    tmp_dist += cur_dist

                    # move to next outer line as this inner line distance already longer than minimum
                    # for faster processing only
                    if tmp_dist > min_dist:
                        break
                prev_inner_obj = inner_obj
            else:
                # skip wtih different medoid for inner obj
                continue
    if tmp_dist < min_dist:
        # return shorter distance and new medoid
        return tmp_dist, tmp_medoid_obj
    # return original minimum distance and None for medoid
    return min_dist, None

def calculateNewMedoids():
    current_medoid_idx = None
    # init min medoid for outer loop
    min_dist = float('inf') # init minimum distance with infinity
    min_medoid_obj = None

    # input comes from STDIN to lines array
    lines = sys.stdin.readlines()
    for line in lines:
        # parse the input of mapper.py
        medoid_idx, curr_obj = convert_line(line)

        # read line all good
        if medoid_idx is not None:
            # init min medoid for outer loop
            tmp_medoid_obj = curr_obj

            if current_medoid_idx == medoid_idx or current_medoid_idx is None:
                # to calculate minimum medoids within the same cluster
                # if None for tmp_min_obj is returned, it means the medoid does not change
                min_dist, tmp_min_obj = calculateMinMedoids(lines, medoid_idx, tmp_medoid_obj, min_dist)
                if tmp_min_obj is not None:
                    min_medoid_obj = tmp_min_obj

                # assign medoid_idx to current_medoid_idx
                current_medoid_idx = medoid_idx
            else:
                # handle diff medoid
                # print out new medoid for a cluster
                print(str(min_medoid_obj[0]) + ", " + str(min_medoid_obj[1]))

                # reset min_dist & min_medoid for next cluster
                min_dist = float('inf')
                min_medoid_obj = None
                current_medoid_idx = medoid_idx
                tmp_medoid_obj = curr_obj

                # to calculate minimum medoids within the same cluster
                min_dist, tmp_min_obj = calculateMinMedoids(lines, medoid_idx, tmp_medoid_obj, min_dist)
                if tmp_min_obj is not None:
                    min_medoid_obj = tmp_min_obj
    
    # print last cluster's medoids
    if current_medoid_idx == medoid_idx and min_dist != float('inf'):
        print(str(min_medoid_obj[0]) + ", " + str(min_medoid_obj[1]))

if __name__ == "__main__":
    calculateNewMedoids()
