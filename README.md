# motion_planning_HW

## [Basic Search Algorithms](Basic Search Algorithms (BFS, DFS, Dijkstra and A-star)/)
## [Standard Search Algorithms](Standard Seach Algorithms (PRM and RRT)/)
## [Advanced Search Algorithms](Advanced Search Algorithms (Informed-RRT-star and D-star)/)


## Basic Search Algorithm

### Test Case 1: When a valid goal is given
After completing the code in the search.py file, the main.py file was run from the command prompt and the following results were obtained:

The following paths were obtained for the testing map file:

### Test Case 2: When a given goal is obstacle



After condition to check if the goal is obstacle was updated the following plots and output were obtained

### Test Case 3: When a given goal is outside the map

Observations:
Test Case 1:
1. We have valid goal position that is within the map and not an obstacle.
2. All the four algorithms were able to reach the goal position and with varying number of steps as follows:
a. Breath-First Search - 64 Steps
b. Depth-First Search - 33 Steps
c. Dijkstra Search - 64 Steps
d. A* Search - 52 Steps
3. It can be observed that the BFS, Dijkstra and A* algorithm follow the same path from start to goal. This is because BFS is the base framework for both Dijkstra and A* algorithm
4. From above it can be observed that both BFS and Dijkstra take the same number of steps. This is usually not the case as Dijkstra algorithm takes a smaller number of steps as well as more optimum path based on the cost-to-come from the start position. In our case the cause to move has been considered as 1 for all the nodes and thus the Dijkstra algorithm becomes similar to the BFS algorithm.
5. DFS algorithm has a different path because it explores branch-wise unlike the other algorithms. Moreover, DFS has a smaller number of steps in this case. The number of steps purely depends on the position of the goal. Had the goal been somewhere in the bottom left corner, then it might have taken much longer step to reach goal.
6. The same above also applies to other algorithms. If the goal is changed, then the algorithms might reach it in different number of steps as seen above.
7. Though A* has same base as BFS and Dijkstra, it takes lesser number of steps to reach the goal because of the heuristics cost, i.e., the cost calculated from the goal to the nodes. It helps the A* algorithm to navigate faster, however the result might be a sub-optimal solution. The corner case where A* can perform poorly compared to other algorithms is when it is stuck in between obstacles. The algorithm might take longer number of steps to come out of it.
Test Case 2:
The goal is assigned to an obstacle, so there is no valid path to be evaluated between the start and the goal nodes. Thus, the as no path is found, the algorithm prints “No path found”
Test Case 3:
The goal is assigned values outside the grid map. Therefore, no valid path can be found in this scenario as well. Thus, the algorithm print “No path found”.


References:
1. BFS Wiki : https://en.wikipedia.org/wiki/Breadth-first_search
2. DFS Wiki : https://en.wikipedia.org/wiki/Depth-first_search
3. Dijkstra Wiki : https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
4. A* Wiki : https://en.wikipedia.org/wiki/A*_search_algorithm
5. RBE550 Motion planning slides
6. Udemy Robotics Course
