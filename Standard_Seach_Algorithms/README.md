# Standard Search Algorithm

## Probabilistic Roadmap (PRM)
The  basic  idea behind  PRM is  to  take  random  samples  from  the  configuration  space  of  the  robot,  testing them  for  whether they  are  in  the  free  space  and  use a  local  planner  to  attempt to  connect these configurations  to other  nearby configurations, if there no  collision in path.  PRM is a multi-query  algorithm. The probabilistic roadmap planner has two  levels:  
 
1. Construction  phase 
2. Query phase 
 
In the  construction  phase,  a roadmap (graph) is built,  approximating the  motions  that  can be  made in  the 
environment.   
1. A random configuration is created.  
2. Then, it is connected  to  some neighbours, typically either the k nearest neighbours  or all neighbours 
less than some predetermined distance.   
3. Configurations and connections  are added to the  graph until the roadmap is dense enough.   
 
In the query  phase, 
1.  The start and goal configurations are connected  to  the graph 
2. The path is obtained  by a Dijkstra's shortest  path query. 

For PRM 4 different sampling methods  have been implemented: 
1. Uniform sampling
<p align="center" width="100%">
    <img width="50%" src=./results/SSA_1.PNG> 
</p> 

2. Random sampling
<p align="center" width="100%">
    <img width="50%" src=./results/SSA_2.PNG> 
</p> 

3. Gaussian sampling 
<p align="center" width="100%">
    <img width="50%" src=./results/SSA_3.PNG> 
</p> 

4. Bridge sampling
<p align="center" width="100%">
    <img width="50%" src=./results/SSA_4.PNG> 
</p>


## Rapidly-exploring Random Tree (RRT)
The  Rapidly-exploring Random Tree (RRT)  is  an  algorithm  designed to  efficiently searching  an  non-convex high-dimensional spaces by randomly building a space-filling tree. The tree is built in steps from a random point sampled in space and there is bias given to the sampling of the random point. In our case, the bias given to the goal to be sampled.  The root of the tree is considered to be the start node and the tree grows from the start position until it reaches the neighbourhood of the goal region.

<p align="center" width="100%">
    <img width="50%" src=./results/SSA_5.PNG> 
</p>

## Rapidly-exploring Random Tree star (RRT*)
RRT* is a variant of the RRT where additional constraints are considered for connection. Like RRT, the sampling of the new node remains the same, but instead of connecting the new node to the nearest node, the neighbours of the new node are considered and the cost-to-come from start for the new node is checked through all  the neighbours. The neighbour that provides the least cost-to-come to the new node is chosen as the parent for the new node. Then the connections are rewired such that the cost-to-come for the neighbours are less than the cost-to-come through the new node, if not the new node is assigned as the parent for the neighbour node.

<p align="center" width="100%">
    <img width="50%" src=./results/SSA_6.PNG> 
</p>


## DISCUSSION
1. For PRM, what are the advantages and dis-advantages if the four sampling methods in comparison to each other? 
    1. Uniform sampling:
        * Advantages: 
          1. Low complexity 
          2. Always ensures to find a path as sample is through the C-space 
        * Disadvantages: 
          1. Computationally expensive as huge number of nodes needs to be explored, which might not be a requirement to find the path. 
    2. Random sampling: 
        * Advantages: 
          1. Low complexity 
        * Disadvantages: 
          1. Fails to find a path sometime if the sampled nodes are not spread or if not close to the goal. 
    3. Gaussian sampling: 
        * Advantages: 
          1. In scenarios where the robot is stuck in between obstacles, it helps to find the path around the obstacles efficiently 
        * Disadvantages: 
          1. It depends on the variance of the Gaussian distribution to  find the nearest point and if the variance is set low, then it samples points very close to each other. 
          2. As the points sampled might be close to each other they might not be able to samples points close to goal, thus not being able to find a feasible path. 
 
    4. Bridge sampling: 
        * Advantages: 
          1. Helps find paths between obstacles in the narrow passages, thus reducing the path length and time to travel.  
          2. Less number of nodes/sample points to deal with and thus computationally less expensive. 
        * Disadvantages: 
          1. If proper radius near the goal is not set, then the goal might not be able to connect with any of the sampled points and thus no path may be found. 
 
2. For RRT, what is the main difference between RRT and RRT*? What changes does it make in terms of efficiency of the algorithms and optimality of the search result? 
    1. The main difference between RRT and RRT* is that, in RRT the new sampled point connects with the nearest node available from the tree irrespective of the cost-to-come, where in case of the RRT*, the neighbour nodes are searched to find the optimum cost-to-come and the new node then connects to that neighbour node. Another major difference is the rewiring of the neighbouring nodes in RRT* with respect to the new node, where as it RRT this doesn’t happen.  
 
    2. Efficiency: If we evaluate efficient with respect to time, then RRT gives an path quickest, but at the same time the path is sub-optimal. On the other hand RRT* algorithm takes a longer time to converge to an  optimal  path as well as  takes more nodes to rewire and connect and thus not efficient with respect to time. 
 
    3. Optimality:  On evaluating  optimality  of  the  algorithm  with  respect to  path,  RRT*  converges to  a optimal path with time when compared to RRT which most of the time returns an sub-optimal path. 
 
3. Comparing between PRM and RRT, what are the advantages and disadvantages? 
 
    1. PRM: 
      * Advantage: 
          1. For  static  environments, PRM can  be  used  to  re-evaluate path is  the  goal  is  changed  in between transversing. The major advantage is that the new path need not be evaluated from beginning  through  sampling  and  a  feasible  path  can  be  obtained  from  already  created connections. 
      * Disadvantage: 
          1. PRM need an optimum range to be set to each for nearest neighbouring node (Local planner), if no connections can be formed then no path can be formed. 
          2. PRM coverage of the entire C-Space entirely depends on the type of sampling we perform in the algorithm and if the sampling method is not suitable for the environment, then maybe no path can be found. 
          3. PRM cannot be used for  Dynamics obstacle environments as re-evaluation of path to  goal becomes computationally very expensive. 
 
    2. RRT: 
      * Advantage: 
          1. RRT can be used to find path in  dynamic obstacle environment. If an obstacle is encounter, a new point can be sampled and the tree can be built around the obstacle thus providing a path.  
          2. RRT can be bias to explore points near the goal or near free space and thus able to cover wider area of the C-space. 
          3. RRT is very efficient in terms of time and thus helpful in real-world scenarios for re-evaluating path when encountered with dynamic obstacle. 
      * Disadvantage: 
          1. RRT give an sub-optimal path most of the time. 


## REFERENCES  
1. Geraerts, R., & Overmars, M. H. (2006). Sampling and node adding in probabilistic roadmap 
planners. Robotics and Autonomous Systems, 54(2), 165–173. 
https://doi.org/10.1016/j.robot.2005.09.026 
 
2. V. Boor, M. H. Overmars and A. F. van der Stappen, "The Gaussian sampling strategy for probabilistic 
roadmap planners," Proceedings 1999 IEEE International Conference on Robotics and Automation 
(Cat. No.99CH36288C), 1999,  pp. 1018-1023  vol.2, doi: 10.1109/ROBOT.1999.772447. 
 
3. D. Hsu, Tingting Jiang, J. Reif and Zheng Sun, "The bridge test for sampling narrow passages with 
probabilistic roadmap planners," 2003  IEEE International Conference on Robotics and Automation 
(Cat. No.03CH37422),  2003, pp. 4420-4426  vol.3, doi: 10.1109/ROBOT.2003.1242285. 
 
4. https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree  
 
5. F. Islam, J. Nasir, U. Malik, Y. Ayaz and O. Hasan, "RRT∗-Smart: Rapid convergence implementation of 
RRT∗ towards optimal solution," 2012  IEEE International Conference on Mechatronics and 
Automation, 2012, pp. 1651-1656,  doi: 10.1109/ICMA.2012.6284384.