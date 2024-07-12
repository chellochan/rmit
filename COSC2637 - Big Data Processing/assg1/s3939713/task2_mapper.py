#!/usr/bin/env python3
"""task2-mapper.py"""

import sys
from math import sqrt

# get initial medoids from a txt file and add them in an array
def getMedoids(filepath):
    medoids = []

    # read medoids from txt file
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line:
                try:
                    line = line.strip()
                    cord = line.split(',')
                    # cord[0] is x and cord[1] is y point of a medoid
                    medoids.append([float(cord[0].strip()), float(cord[1].strip())])
                except:
                    break
            else:
                break
            line = fp.readline()
    fp.close()
    return medoids

# create clusters based on initial medoids
def createClusters(medoids):
    # 
    for line in sys.stdin:
        line = line.strip()
        cord = line.split(',')[4:6] # only extract pickup_x and pickup_y of Trips.txt
        min_dist = float('inf') # init minimum distance with infinity
        index = -1

        try:
            cord[0] = float(cord[0])
            cord[1] = float(cord[1])
        except ValueError:
            # float was not a number, so silently
            # ignore/discard this line
            continue

        for medoid in medoids:
            # euclidian distance from every point of dataset
            # to every medoid
            cur_dist = sqrt(pow(cord[0] - medoid[0], 2) + pow(cord[1] - medoid[1], 2))

            # find the medoid which is closer to the point
            if cur_dist <= min_dist:
                min_dist = cur_dist
                index = medoids.index(medoid)

        var = "%s\t%s\t%s" % (index, cord[0], cord[1])
        print(var)

if __name__ == "__main__":
    medoids = getMedoids('medoids.txt')
    createClusters(medoids)
