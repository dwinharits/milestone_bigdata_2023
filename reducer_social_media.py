#! /home/bigdata/anaconda3/bin/python3

import sys

count = 0
oldDate = None
oldKey = None

for line in sys.stdin:
    row = line.strip().split('\t')

    if len(row) != 2:
        continue

    thisKey, thisDate = row

    if oldKey and oldDate and (oldKey != thisKey or oldDate != thisDate):
        print("%s\t%s\t%s" % (oldKey, oldDate, count))
        count = 0

    oldKey = thisKey
    oldDate = thisDate
    count += 1

if oldKey != None:
    print("%s\t%s\t%s" % (oldKey, oldDate, count))