#!/usr/bin/env python3
import sys
# Task 3 subtask mapper join
# this subtask reads both Taxis.txt and Trips.txt and extract their meaningful attributes
# i.e. Taxi#, company from Taxis.txt and Taxi#, Trip# from Trips.txt

for line in sys.stdin:
    line = line.strip()
    splits = line.split(",") # spliting fields with separators ","
    
    try:
        # Use no. of splits to distinguish the line is from which documents.
        if len(splits) == 4: # Taxi 
            splits[0] = int(splits[0]) # Taxi#
            splits[1] = int(splits[1]) # company
            # stdout all lines with new formats "Taxi#,company,Trip"
            # use "~" to represent empty value
            print('%d,%d,%s' % (splits[0],splits[1],"~"))
        else: # Trip
            splits[1] = int(splits[1]) # Taxi#
            splits[0] = int(splits[0]) # Trip#
            # stdout all lines with new formats "Taxi#,company,Trip"
            # use "~" to represent empty value
            print('%d,%s,%d' % (splits[1],"~",splits[0]))
    except:
        continue