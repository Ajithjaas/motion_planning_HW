# RBE 550 - Advanced Search Algorithms Implementation

## Informed-RRT* Algorithm
The  basic  idea  behind  the  INFORMED  RRT*  is  additional  constraints  in  the  sampling process. Initially, the informed RRT* starts with the same process as the RRT* algorithm. Like RRT* the new node is connected to the nearest node. Then the neighbors of the new node are considered and the cost-to-come from start to the new node is checked through all the neighbors. The neighbor that provides the least cost-to-come to the new node is chosen as the parent for the new node. Then the connections are rewired such that the cost-to-come for the neighbors are less than the cost-to-come through the new node, if not the new node is assigned as the parent for the neighbor node.

After  the  path  is  found,  then  the  sampling  process  is  changed.  Instead  of  sampling randomly from the entire space, the sampling is restricted to an ellipse (or ellipsoid in 3D) with the focal points being the start and the end nodes. 

<p align="center" width="100%">
    <img width="30%" src=./results/ASA_3.PNG> 
</p>

Based on this restricted sampling, a new point is obtained. This new point is then used to rewire and replan the entire path. The following is the path for three algorithms, namely RRT, RRT* and Informed-RRT* :

<p align="center" width="100%">
    <img width="80%" src=./results/ASA_1.PNG> 
</p>

From the above plots it can be observed that the informed RRT* star has spread in a smaller region compared to the RRT* as well as both RRT* and informed RRT* have shorter path than the RRT algorithm. This can be observed from the below output:
<p align="center" width="100%">
    <img width="80%" src=./results/ASA_5.PNG> 
</p>

## D* Algorithm
In  this  section,  the  implementation  of  D*  is  discussed.  Like  Dijkstra  or  A*,  D*  algorithm  also maintains an open list. Each node has a different state tag as follows:  
  1. NEW 
  2. OPEN  
  3. CLOSED  
  4. RAISE  
  5. LOWER 

Based  on each tag,  the  nodes  are  processed  using  the  Process_State  function.  In  Process_State function, we initialize the goal’s heuristic as zero and then insert into the open list. The function is called until robot’s state is removed from the open list.  During  each  process  state,  the Prepare_Repair function is called. This function checks if the neighbours of the current state is an obstacle or not. If the one of the neighbours is an obstacle.

If one of the neighbours  is observed to be an obstacle in the Prepare_Repair function, then the Modify_cost function is called. This function modified the neighbours cost according to the new obstacles. After the neighbours cost are modified, then the Repair-Replan function is called which takes care of repairing the cost of the neighbours by replanning the path. 

<p align="center" width="100%">
    <img width="80%" src=./results/ASA_2.gif> 
</p>

The out put for the above scenario is as follows:
<p align="center" width="100%">
    <img width="80%" src=./results/ASA_6.PNG> 
</p>


# DISCUSSION
### Difference between RRT* and Informed-RRT*
<p align="center" width="100%">
    <img width="80%" src=./results/ASA_4.PNG> 
</p>

### D* vs A* or Dijkstra 
1. A* and Dijkstra are used for static environment whereas D* is used for dynamic environment. 
2. In case we use A* and Dijkstra in the dynamic environment, then the entire path must be replanned from  the  current  position  to  the  goal  position.  During  this, the  entire  environment  is  again  re-evaluated. Whereas in the case of the D* algorithm, the changes are made locally when the obstacle is  faced  and  based  on  the change,  a  different  path is  followed  which is  optimum  from  the changed direction. Thus, it can be observed that A* and Dijkstra are computationally more expensive than D*. Therefore, D* is comparatively faster than A* and Dijkstra algorithm. 