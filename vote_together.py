import csv
import sys

import numpy


reader = csv.reader(sys.stdin)
alders = numpy.array(next(reader)[3:])

votes = numpy.array(list(reader))
votes = votes[:, 3:]

votes = (votes == 'no').astype(int)

vote_together = numpy.dot(votes.T, votes)

u, s, vh = numpy.linalg.svd(vote_together)

dim_1 = numpy.argsort(u[:, 0])
dim_2 = numpy.argsort(u[:, 1])

vote_together = vote_together[dim_1, :][:, dim_1]

writer = csv.writer(sys.stdout)

writer.writerow([''] + list(alders[dim_1]))
for alder, row in zip(alders[dim_1], vote_together):
    writer.writerow([alder] + list(row.astype(str)))

