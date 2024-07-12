#!/usr/bin/env python3
import sys

# Task 3 subtask reducer
# this subtask reduces the lines from mapper (actually is from reducer-join as mapper did nothing) 
# by aggregatting the count by same company
# a line represents the count of trips from a taxi with its company
# this reducer to aggregrate the trip count for each company
# output format company,count
# the output of each line represents a trip count of each company

# param initialzation
current_company = None
total_count = 0

for line in sys.stdin:
    line = line.strip()
    company, count = line.split(",") # Line format: <company>,<count>

    if current_company != company:
        if current_company is not None: # to exclude None company count (i.e. the first line)
            # output the company of previous line and its count as the previous line is not the same company
            print('%s,%d' % (current_company, total_count))
        # assign this line to current attribute and reset counter
        current_company = company
        total_count = int(count)
    else:
        # if the current line company (i.e. company) is same as previous line company (i.e. current_company),
        # aggregate the count 
        try:
            # convert count to int
            count = int(count)
            total_count += count
        except:
            continue

# to print the last taxi count
if current_company == company:
    print('%s,%d' % (current_company, total_count))