from grid import *
from solver import *

cases = open("testcases.txt", "r")
succeeded, failed = 0, 0
for case in cases:
	values = case.strip().split("|")
	width, height = int(values[0].strip()), int(values[1].strip())
	islands = eval(values[2].strip())
	s = Solver(width, height, islands)
	if s.search() == 1:
		succeeded += 1
		print("SOLVED")
	else:
		failed += 1
		print("FAILURE")
	print(s)
cases.close()
print("Succeeded: {0} | Failed: {1}".format(succeeded, failed))