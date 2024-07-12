#!/usr/bin/env python3
import sys
# Task 1 count the number of trips and the average distance pre trip for each taxi
for line in sys.stdin:
    line = line.strip()
    trip = line.split(",")

    try:
        if trip[1].strip() and trip[3].strip(): #trip[1] is taxi no while trip[3] is distance
            trip[1] = int(trip[1])
            trip[3] = float(trip[3])
            print('%d\t%f' % (trip[1],trip[3]))
    except:
        continue