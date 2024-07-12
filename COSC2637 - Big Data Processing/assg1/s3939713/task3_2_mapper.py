#!/usr/bin/env python3
import sys
# Task 3 part 2 mapper
# format <company>,<count>
# nothing to change for this mapper
# just stdout the same to partioner, sorter and reducer.

for line in sys.stdin:
    line = line.strip()
    company, count = line.split(",") # Line format: <company>,<count>

    try:
        if company.strip() and count.strip():
            company= int(company)
            count = int(count)
            print('%d,%d' % (company, count))
    except:
        continue