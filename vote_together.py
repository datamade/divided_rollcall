import csv
import sys

import numpy


reader = csv.reader(sys.stdin)

alders = numpy.array(next(reader)[3:])

votes = numpy.array(list(reader))
votes = votes[:, 3:]

no_votes = -((votes == 'no').astype(int))
yes_votes = (votes == 'yes').astype(int)

votes = no_votes + yes_votes

u, s, vh = numpy.linalg.svd(votes.T)

dim_1 = numpy.argsort(u[:, 0])
dim_2 = numpy.argsort(-u[:, 1])

oppose_together = numpy.dot(no_votes.T, no_votes)

oppose_together = oppose_together[dim_2, :][:, dim_2]

writer = csv.writer(sys.stdout)

writer.writerow([''] + list(alders[dim_2]))
for alder, row in zip(alders[dim_2], oppose_together):
     writer.writerow([alder] + list(row.astype(str)))

