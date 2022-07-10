# Standard Algorithm Implementation
# Sampling-based Algorithms PRM

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from scipy.spatial import KDTree


# Class for PRM
class PRM:
    # Constructor
    def __init__(self, map_array):
        self.map_array = map_array            # map array, 1->free, 0->obstacle
        self.size_row = map_array.shape[0]    # map size
        self.size_col = map_array.shape[1]    # map size

        self.samples = []                     # list of sampled points
        self.graph = nx.Graph()               # constructed graph
        self.path = []                        # list of nodes of the found path


    def check_collision(self, p1, p2):
        '''Check if the path between two points collide with obstacles
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            True if there are obstacles between two points
        '''
        flag = False
        if abs(p1[0]-p2[0]) > abs(p1[1]-p2[1]):
            x = np.linspace(p1[0],p2[0],abs(p2[0]-p1[0])+1).astype(int)
            y = np.round(np.linspace(p1[1],p2[1],abs(p2[0]-p1[0])+1)).astype(int)
        else:
            x = np.round(np.linspace(p1[0],p2[0],abs(p2[1]-p1[1])+1)).astype(int)
            y = np.linspace(p1[1],p2[1],abs(p2[1]-p1[1])+1).astype(int)            
            
        for i,j in zip(x,y):
            if self.map_array[i,j] == 0:
                flag = True
                
        return flag


    def dis(self, point1, point2):
        '''Calculate the euclidean distance between two points
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            euclidean distance between two points
        '''
        point1 = np.array(point1)
        point2 = np.array(point2)
        return np.linalg.norm(point1 - point2)

    def uniform_sample(self, n_pts):
        '''Use uniform sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        ## Initialize graph
        self.graph.clear()
        sample_row = np.linspace(0,self.size_row-1,int(np.sqrt(n_pts))).astype(int)
        sample_col = np.linspace(0,self.size_col-1,int(np.sqrt(n_pts))).astype(int)        
        for i in sample_row:
            for j in sample_col:
                if self.map_array[i,j] == 1 :
                    self.samples.append((i,j))

    
    def random_sample(self, n_pts):
        '''Use random sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        x = np.random.randint(0,self.size_row,n_pts)
        y = np.random.randint(0,self.size_col,n_pts)       
        
        sample_list = []
        samples  = [(x[i],y[i]) for i in range(n_pts)]
        for sample in samples:
            if sample in sample_list:
                continue
            else:
                sample_list.append(sample)

        for sample in sample_list :
            if self.map_array[sample[0],sample[1]] == 1:
                self.samples.append((sample[0],sample[1]))

        

    def gaussian_sample(self, n_pts):
        '''Use gaussian sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        i=0
        while i < n_pts:
            x1 = int(np.random.randint(0,(self.size_row-1),1))
            y1 = int(np.random.randint(0,(self.size_col-1),1))       
            
            x2 = int(np.round(np.random.normal(x1, 10, 1)))
            y2 = int(np.round(np.random.normal(y1, 10, 1)))
            
            if x2 > self.size_row-1:
                x2 = self.size_row-1
            if x2 < 0:
                x2 = 0    
            if y2 > self.size_col-1:
                y2 = self.size_col-1
            if y2 < 0:
                y2 = 0
        
            #l.append([x1,y1,x2,y2])
            # print('\nx1: ',x1,"\ty1: ",y1,'\tx2: ',x2,"\ty2: ",y2)
 
            if (self.map_array[x1,y1] == 0 and self.map_array[x2,y2] == 0) or (self.map_array[x1,y1] == 1 and self.map_array[x2,y2] == 1):
                continue
            elif self.map_array[x1,y1] == 0 and self.map_array[x2,y2] == 1 and (x2,y2) not in self.samples:
                self.samples.append((x2,y2))
            elif self.map_array[x1,y1] == 1 and self.map_array[x2,y2] == 0 and (x1,y1) not in self.samples:
                self.samples.append((x1,y1))
                
            i = i+1
                    
            


    def bridge_sample(self, n_pts):
        '''Use bridge sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        i=0
        while i < n_pts:
            x1 = int(np.random.randint(0,(self.size_row-1),1))
            y1 = int(np.random.randint(0,(self.size_col-1),1))       

            if self.map_array[x1,y1] == 0:
                x2 = int(np.round(np.random.normal(x1, 20, 1)))
                y2 = int(np.round(np.random.normal(y1, 20, 1)))
                
                if x2 > self.size_row-1:
                    x2 = self.size_row-1
                if x2 < 0:
                    x2 = 0    
                if y2 > self.size_col-1:
                    y2 = self.size_col-1
                if y2 < 0:
                    y2 = 0

                if self.map_array[x2,y2] == 0:                     
                    x_mid = int((x2+x1)/2)
                    y_mid = int((y2+y1)/2)
                    
                    if self.map_array[x_mid,y_mid] == 1 and (x_mid,y_mid) not in self.samples:
                        self.samples.append((x_mid,y_mid))                
                    
            i = i+1
        

    def draw_map(self):
        '''Visualization of the result
        '''
        # Create empty map
        fig, ax = plt.subplots()
        img = 255 * np.dstack((self.map_array, self.map_array, self.map_array))
        ax.imshow(img)

        # Draw graph
        # get node position (swap coordinates)
        node_pos = np.array(self.samples)[:, [1, 0]]
        pos = dict( zip( range( len(self.samples) ), node_pos) )
        pos['start'] = (self.samples[-2][1], self.samples[-2][0])
        pos['goal'] = (self.samples[-1][1], self.samples[-1][0])
        
        # draw constructed graph
        nx.draw(self.graph, pos, node_size=3, node_color='y', edge_color='y' ,ax=ax)

        # If found a path
        if self.path:
            # add temporary start and goal edge to the path
            final_path_edge = list(zip(self.path[:-1], self.path[1:]))
            nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=self.path, node_size=8, node_color='b')
            nx.draw_networkx_edges(self.graph, pos=pos, edgelist=final_path_edge, width=2, edge_color='b')

        # draw start and goal
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['start'], node_size=12,  node_color='g')
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['goal'], node_size=12,  node_color='r')

        # show image
        plt.axis('on')
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.show()


    def sample(self, n_pts=1000, sampling_method="uniform"):
        '''Construct a graph for PRM
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            sampling_method - name of the chosen sampling method

        Sample points, connect, and add nodes and edges to self.graph
        '''
        # Initialize before sampling
        self.samples = []
        self.graph.clear()
        self.path = []
        global r

        # Sample methods
        if sampling_method == "uniform":
            self.uniform_sample(n_pts)
            r = 15
        elif sampling_method == "random":
            self.random_sample(n_pts)
            r = 20
        elif sampling_method == "gaussian":
            self.gaussian_sample(n_pts)
            r = 10
        elif sampling_method == "bridge":
            self.bridge_sample(n_pts)
            r = 22

        ### YOUR CODE HERE ###
        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # Store them as
        # pairs = [(p_id0, p_id1, weight_01), (p_id0, p_id2, weight_02), 
        #          (p_id1, p_id2, weight_12) ...]

        pairs = []
        kdtree  = KDTree(self.samples)
        pair    = list(kdtree.query_pairs(r))
        for (i,j) in pair:
            point1  = list(self.samples[i])
            point2  = list(self.samples[j])
            dist    = self.dis(point1,point2)
            flag    = self.check_collision(point1, point2)

            if flag == False and (i,j,dist) not in pairs and (i != j):
                pairs.append((i,j,dist))
        
        if sampling_method == "gaussian":
            r = 60
        elif sampling_method == "bridge":
            r = 100
            
        # Use sampled points and pairs of points to build a graph.
        # To add nodes to the graph, use
        # self.graph.add_nodes_from([p_id0, p_id1, p_id2 ...])
        # To add weighted edges to the graph, use
        # self.graph.add_weighted_edges_from([(p_id0, p_id1, weight_01), 
        #                                     (p_id0, p_id2, weight_02), 
        #                                     (p_id1, p_id2, weight_12) ...])
        # 'p_id' here is an integer, representing the order of 
        # current point in self.samples
        # For example, for self.samples = [(1, 2), (3, 4), (5, 6)],
        # p_id for (1, 2) is 0 and p_id for (3, 4) is 1.
        self.graph.add_nodes_from([])
        self.graph.add_weighted_edges_from(pairs)
        # Print constructed graph information
        n_nodes = self.graph.number_of_nodes()
        n_edges = self.graph.number_of_edges()
        print("The constructed graph has %d nodes and %d edges" %(n_nodes, n_edges))


    def search(self, start, goal):
        '''Search for a path in graph given start and goal location
        arguments:
            start - start point coordinate [row, col]
            goal - goal point coordinate [row, col]

        Temporary add start and goal node, edges of them and their nearest neighbors
        to graph for self.graph to search for a path.
        '''
        # Clear previous path
        self.path = []

        # Temporarily add start and goal to the graph
        self.samples.append(start)
        self.samples.append(goal)
        # start and goal id will be 'start' and 'goal' instead of some integer
        self.graph.add_nodes_from(['start', 'goal'])

        ### YOUR CODE HERE ###

        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # You could store them as
        # start_pairs = [(start_id, p_id0, weight_s0), (start_id, p_id1, weight_s1), 
        #                (start_id, p_id2, weight_s2) ...]
        start_pairs = []
        goal_pairs = []

        kdtree  = KDTree(self.samples)
        index   = kdtree.query_ball_point(start,r)
        for i in index:
            point1  = list(start)
            point2  = list(self.samples[i])
            dist    = self.dis(point1,point2)
            flag    = self.check_collision(point1, point2)
            
            if flag == False and ('start',i,dist) not in start_pairs and ('start' != i):
                start_pairs.append(('start',i,dist))

        index   = kdtree.query_ball_point(goal,r)
        for i in index:
            point1  = list(goal)
            point2  = list(self.samples[i])
            dist    = self.dis(point1,point2)
            flag    = self.check_collision(point1, point2)

            if flag == False and ('goal',i,dist) not in start_pairs and ('goal' != i):
                goal_pairs.append(('goal',i,dist))

        # Add the edge to graph
        self.graph.add_weighted_edges_from(start_pairs)
        self.graph.add_weighted_edges_from(goal_pairs)
        
        # Seach using Dijkstra
        try:
            self.path = nx.algorithms.shortest_paths.weighted.dijkstra_path(self.graph, 'start', 'goal')
            path_length = nx.algorithms.shortest_paths.weighted.dijkstra_path_length(self.graph, 'start', 'goal')
            print("The path length is %.2f" %path_length)
        except nx.exception.NetworkXNoPath:
            print("No path found")
        
        # Draw result
        self.draw_map()

        # Remove start and goal node and their edges
        self.samples.pop(-1)
        self.samples.pop(-1)
        self.graph.remove_nodes_from(['start', 'goal'])
        self.graph.remove_edges_from(start_pairs)
        self.graph.remove_edges_from(goal_pairs)
        
