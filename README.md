### Bridges solver

This is the code behind this [Bridges solver](https://alextseng.net/projects/bridges/).

The code needed to run the solver is in `grid.py` and `solver.py`.

Test cases are in `testcases.txt`. To run the test cases, run `run_test_cases.py`. The script `make_testcase.py` can help a user easily create a test case through a GUI.

The general algorithm is a depth-first search tree (i.e. guess a move and recursively solve; if we end up in a deadlock or a failed state, then backtrack and guess again). This search is greatly accelerated by applying logical steps to the grid whenever possible (i.e. placing bridges for which we are certain given the current state of the grid).
