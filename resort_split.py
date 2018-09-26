import csv
import sys

import numpy

reader = csv.reader(sys.stdin)

header = next(reader)
alders = numpy.array(header[3:])

raw_votes = list(reader)
votes = numpy.array(raw_votes)
votes = votes[:, 3:]

no_votes = -((votes == 'no').astype(int))
yes_votes = (votes == 'yes').astype(int)

votes = no_votes + yes_votes

u, s, vh = numpy.linalg.svd(votes.T)

dim_1_j = numpy.argsort(u[:, 0])
dim_2_j = numpy.argsort(-u[:, 1])

dim_1_i = numpy.argsort(vh[0, :])
dim_2_i = numpy.argsort(vh[1, :])

writer = csv.writer(sys.stdout)

writer.writerow(header[:3] + list(alders[dim_2_j]))
for i in dim_2_i:
     vote = raw_votes[i]
     item, options = vote[:3], vote[3:]
     row = item + [options[j] for j in dim_2_j]
     writer.writerow(row)

