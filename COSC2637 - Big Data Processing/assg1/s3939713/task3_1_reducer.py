#!/usr/bin/env python3
import sys

# Task 3 subtask join reducer
# this subtask reduces the lines from mapper-join by aggregatting the count by same taxi
# as a taxi is only belongs to a company, the count of each taxi can be represented with company as key
# output format company,count
# each line represents a single taxi count of trip

current_company = None
current_taxi = None
count = 0
for line in sys.stdin:
    line = line.strip()
    taxi,company,trip = line.split(",")    # Taxi#,company,Trip


    if current_taxi != taxi:
        if current_taxi is not None: # to exclude None company count (i.e. the first line)
            # output the taxi of previous line and its count as the previous line is not the same taxi
            print('%s,%d' % (current_company, count))
        # assign this line to current attribute and reset counter
        current_taxi = taxi
        current_company = company
        count = 0

    # "~" is the empty value
    # if company is empty, it means the line is from trip
    # therefore, it should be count as 1 trip
    if company == "~":
        count += 1

# to print the last taxi count
if current_taxi == taxi:
    print('%s,%d' % (current_company, count))