# Basic searching algorithms
import math

# Class for each node in the grid
class Node:
    def __init__(self, row, col, is_obs, h):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.is_obs = is_obs  # obstacle?
        self.g = None         # cost to come (previous g + moving cost)
        self.h = h            # heuristic
        self.cost = None      # total cost (depend on the algorithm)
        self.parent = None    # previous node

# Function to create a graph of nodes for the given grid map
def init_graph(grid,source):  
    graph = []
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            node = Node(i,j,False,False)
            # checking if the node is the source node
            if node.row == source.row and node.col == source.col:
                node.g      = 0         # If the node is the source node intializing cost to 0 
                node.cost   = 0         
            else:
                node.g      = math.inf  # The initial cost-to-come is set as infintiy
                node.cost   = math.inf  # The initial total cost is set as infinity
            # checking if the node is an obstacle
            if grid[i][j]>0:
                node.is_obs = True
            # Appending the node to the graph
            row.append(node)
        graph.append(row)
    
    return graph


# Function to seach if a node is present in the explored list
def search_explored(node,explored):
    flag = False
    for n in explored:
        if n.col == node.col and n.row == node.row :
            flag = True
            break 
    return flag

# Funtion to initialize the heuristic function (i.e. Manhattan distance) for the A-star algorithm
def heuristic(graph,end):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            graph[i][j].h = abs(graph[i][j].row-end.row) + abs(graph[i][j].col-end.col)
    return graph



def bfs(grid, start, goal):
    '''
    Return a path found by BFS alogirhm 
    and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. c
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> bfs_path, bfs_steps = bfs(grid, start, goal)
    It takes 10 steps to find a path using BFS
    >>> bfs_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False
    
    #Initializing the start and end node
    source      = Node(start[0],start[1],False,False)
    end         = Node(goal[0],goal[1],False,False)


    # Checking the corner cases for the goal location     
    if goal[0] >= len(grid) or goal[1] >= len(grid[0]) or goal[0]<0 or goal[1]<0:
        end.is_obs = True 
    else:
        if grid[goal[0]][goal[1]]>0:
            end.is_obs = True
            
    # Calling the function to convert the grid into graph of nodes
    graph       = init_graph(grid,source)

    # Initializing the explored and queue lists
    explored    = [graph[source.row][source.col]] 
    queue       = [graph[source.row][source.col]]

    while  len(queue) > 0:
        current_node = queue.pop(0) # Popping the first node and storing it as the current node
        
        if end.is_obs == True: # checking if the goal is a corner case condition and if so the loop exits
            break
        
        steps = steps + 1   # Calculating the number of step 
        
        # Checking if the current node is the goal node or not
        if current_node.row == end.row and current_node.col == end.col:
            found = True
            break     
        
        row = current_node.row
        col = current_node.col
        
        # Cheking if condition for the neighbouring nodes to be added to the queue
        for k in [[row,col+1],[row+1,col],[row,col-1],[row-1,col]]:
            if k[1] < len(graph[row]) and k[0] < len(graph) and k[1]>= 0 and k[0]>= 0 and graph[k[0]][k[1]].is_obs == False and search_explored(graph[k[0]][k[1]],explored)==False :
                node = graph[k[0]][k[1]] 
                node.parent = current_node 
                explored.append(node) 
                queue.append(node)

    # Tracing back the path from the goal node to the start node
    n = current_node 
    while n != graph[source.row][source.col]:
        path.append([n.row,n.col])
        n = n.parent    
    path.append([graph[source.row][source.col].row,graph[source.row][source.col].col])
    path  = path[::-1] 
 
    if found:
        print(f"It takes {steps} steps to find a path using BFS")
    else:
        print("No path found")
                
    return path, steps


def dfs(grid, start, goal):
    '''Return a path found by DFS alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> dfs_path, dfs_steps = dfs(grid, start, goal)
    It takes 9 steps to find a path using DFS
    >>> dfs_path
    [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 3], [3, 3], [3, 2], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False

    #Initializing the start and end node
    source      = Node(start[0],start[1],False,False)
    end         = Node(goal[0],goal[1],False,False)
    
    # Checking the corner cases for the goal location 
    if goal[0] >= len(grid) or goal[1] >= len(grid[0]) or goal[0]<0 or goal[1]<0:
        end.is_obs = True 
    else:
        if grid[goal[0]][goal[1]]>0:
            end.is_obs = True
    
    # Calling the function to convert the grid into graph of nodes
    graph       = init_graph(grid,source)

    # Initializing the explored and queue lists 
    explored    = []
    stack       = [graph[source.row][source.col]]

    while  len(stack) > 0:
        current_node = stack.pop() # Removing the top node from the stack
        

        if end.is_obs == True: # checking if the goal is a corner case condition and if so the loop exits
            break
        
        # Checking if current node is already an explored node 
        if search_explored(current_node,explored) == True:
            continue
        
        # Calculating the steps
        steps = steps + 1  

        # Checking if the current node is the goal node    
        if current_node.row == end.row and current_node.col == end.col:
            found = True
            break     
        
        # Adding currrent node to the explored list
        explored.append(current_node)
        
        row = current_node.row
        col = current_node.col
        
        # Checking condition for neighbours and updating the nodes 
        for k in [[row-1,col],[row,col-1],[row+1,col],[row,col+1]]:
            if k[1] < len(graph[row]) and k[0] < len(graph) and k[1]>= 0 and k[0]>= 0 and graph[k[0]][k[1]].is_obs == False and search_explored(graph[k[0]][k[1]],explored)==False :
                node = graph[k[0]][k[1]] 
                node.parent = current_node
                stack.append(node)

    # Retracing the path from goal to start nodes                 
    n = current_node 
    while n != graph[source.row][source.col]:
        path.append([n.row,n.col])
        n = n.parent
    path.append([graph[source.row][source.col].row,graph[source.row][source.col].col])
    path  = path[::-1] 
    
    if found:
        print(f"It takes {steps} steps to find a path using DFS")
    else:
        print("No path found")

    return path, steps




def dijkstra(grid, start, goal):
    '''Return a path found by Dijkstra alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> dij_path, dij_steps = dijkstra(grid, start, goal)
    It takes 10 steps to find a path using Dijkstra
    >>> dij_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False

    # Initializing the start and goal nodes
    source      = Node(start[0],start[1],False,False)
    end         = Node(goal[0],goal[1],False,False)
    
    # checking if the goal is a corner case condition and assigning it as a obstacle
    if goal[0] >= len(grid) or goal[1] >= len(grid[0]) or goal[0]<0 or goal[1]<0:
        end.is_obs = True 
    else:
        if grid[goal[0]][goal[1]]>0:
            end.is_obs = True
    
    # Calling a function to create graph of nodes from the grid
    graph       = init_graph(grid,source)

    # Initiliazing the queue with the start node
    queue       = [graph[source.row][source.col]]
    
    while  len(queue) > 0:
        queue = sorted(queue, key=lambda x:x.g) # Sorting the queue in the ascending order of cost of nodes
        current_node = queue.pop(0) # Removing the first element of the queue and exploring it

        # Checking if the goal node is an obstacle and if so the loop exits          
        if end.is_obs == True:
            break
        
        # Calculating the steps
        steps = steps + 1 
        
        # Checking if the curren node is the goal node and if so the loop terminates
        if current_node.row == end.row and current_node.col == end.col:
            found = True
            break     
        
        row = current_node.row
        col = current_node.col
        
        # Checking the neighbour condition for the current node and updating the neighbour nodes
        for k in [[row,col+1],[row+1,col],[row,col-1],[row-1,col]]:
            if k[1] < len(graph[row]) and k[0] < len(graph) and k[1]>= 0 and k[0]>= 0 and graph[k[0]][k[1]].is_obs == False :
                node = graph[k[0]][k[1]] 
                if current_node.g+1 < node.g: # Checking if the cost of the neighbour node is greater than the cost from the curren node
                    node.parent = current_node
                    node.g = current_node.g + 1
                    queue.append(node)

    # Retracing the path from the goal node to the start node                
    n = current_node 
    while n != graph[source.row][source.col]:
        path.append([n.row,n.col])
        n = n.parent
    path.append([graph[source.row][source.col].row,graph[source.row][source.col].col])
    path  = path[::-1] 
    
    if found:
        print(f"It takes {steps} steps to find a path using Dijkstra")
    else:
        print("No path found")
    return path, steps


def astar(grid, start, goal):
    '''Return a path found by A* alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> astar_path, astar_steps = astar(grid, start, goal)
    It takes 7 steps to find a path using A*
    >>> astar_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False

    # Initializing the start and goal nodes
    source      = Node(start[0],start[1],False,False)
    end         = Node(goal[0],goal[1],False,False)
    
    # checking if the goal is a corner case  and initializing it as an obstacle
    if goal[0] >= len(grid) or goal[1] >= len(grid[0]) or goal[0]<0 or goal[1]<0:
        end.is_obs = True 
    else:
        if grid[goal[0]][goal[1]]>0:
            end.is_obs = True
    
    # Creating the graph of nodes from the grid
    graph       = init_graph(grid,source)

    # Initializing all the heuristic variable values for each node
    graph       = heuristic(graph, end)
    
    # Initializing the queue with the start node
    queue       = [graph[source.row][source.col]]
    
    while  len(queue) > 0:
        queue = sorted(queue, key=lambda x:x.cost) # Sorting the queue based on the total function i.e. cost-to-come + heuristic
        current_node = queue.pop(0) # Removing the first element from the queue to be explored
        
        # Checking if the goal node is an obstacle and if so the loop terminates
        if end.is_obs == True:
            break
        
        # Calculating the number of steps
        steps = steps + 1 
        
        # Checking if the current node is the goal and if so the loop terminates 
        if current_node.row == end.row and current_node.col == end.col:
            found = True
            break     
        
        row = current_node.row
        col = current_node.col
        
        # Checking the condition for the neighbours and updating the node information
        for k in [[row,col+1],[row+1,col],[row,col-1],[row-1,col]]:
            if k[1] < len(graph[row]) and k[0] < len(graph) and k[1]>= 0 and k[0]>= 0 and graph[k[0]][k[1]].is_obs == False :
                node = graph[k[0]][k[1]] 
                if (current_node.g+1) < node.g:            # Checking if the cost of the neighbour node is greater than the cost from the curren node
                    node.parent = current_node
                    node.g      = current_node.g + 1
                    node.cost   = node.g + node.h 
                    queue.append(node)

    # Retracing the path from goal to start        
    n = current_node 
    while n != graph[source.row][source.col]:
        path.append([n.row,n.col])
        n = n.parent
    path.append([graph[source.row][source.col].row,graph[source.row][source.col].col])
    path  = path[::-1] 
    
    if found:
        print(f"It takes {steps} steps to find a path using A*")
    else:
        print("No path found")
    return path, steps


# Doctest
if __name__ == "__main__":
    # load doc test
    from doctest import testmod, run_docstring_examples
    # Test all the functions
    testmod()
