#!/usr/bin/env python3
import sys

# init var
current_taxi = None
current_distance = 0.0
taxi = None
count = 0

# read lines from sorted mapper
for line in sys.stdin:
    line = line.strip()
    taxi,distance = line.split('\t')

    try:
        distance = float(distance)
    except ValueError:
        # trash lines if distance cannot be converted to float quietly
        continue

    if current_taxi == taxi:
        # sum up distance and add counter for same taxi
        current_distance += distance
        count += 1
    else:
        # output taxi, count, average distance in 2 decimal places
        if current_taxi:
            print('%s,%d,%.2f' % (current_taxi, count, current_distance/count))
        current_distance = distance
        current_taxi = taxi
        count = 1

# print last row
if current_taxi == taxi:
    print('%s,%d,%.2f' % (current_taxi, count, current_distance/count))