import random as rd

class Environment:
    def __init__(self, width, height, nest_w, nest_h, food_clusters, food_cluster_size, obstacle_clusters, obstacle_cluster_size, min_obj, max_obj):
        self.width = width
        self.height = height
        self.grid = [['empty' for _ in range(width)] for _ in range(height)] #all cells are initialized empty
        self.nest = [nest_h, nest_w] #the "ant nest" is located at the middle of the given environment
        self.grid[self.nest[0]][self.nest[1]] = 'nest' #the grid of the nest is marked as such and not as "empty"
        self.food_clusters = food_clusters
        self.food_cluster_size = food_cluster_size
        self.obstacle_clusters = obstacle_clusters
        self.obstacle_cluster_size = obstacle_cluster_size
        self.min_obj = min_obj
        self.max_obj = max_obj
        self.generate_objects_clusters()

    def is_inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_objects_clusters(self):
        """
        Generate a random environment with objects scattered in clusters around the environment, depending on the configuration parameters.
        """
        clusters_dimensions = [
                                ['food', self.food_clusters, self.food_cluster_size],
                                ['obstacle', self.obstacle_clusters, self.obstacle_cluster_size]
        ] #..._clusters is the number of clusters, ..._cluster_size is the maximum distance of an object to the center of its cluster
        for object, nb_clusters, max_dist_cluster in clusters_dimensions: #for every type of object
            for _ in range(nb_clusters):
                cX, cY = rd.randrange(self.width), rd.randrange(self.height) # randomly choose the center of the cluster
                for _ in range(rd.randint(self.min_obj, self.max_obj)): #randomly choose the number of objects between the min and max of objects defined (TODO min might not be respected if object is out of bounds)
                    odX = rd.randint(-max_dist_cluster, max_dist_cluster)
                    odY = rd.randint(-max_dist_cluster, max_dist_cluster)
                    oX, oY = cX+odX, cY+odY
                    if (0<=oX<self.width 
                        and 0<=oY<self.height
                        and self.grid[oY][oX]=='empty'):
                            self.grid[oY][oX]= object
    
    def get_type(self, x, y):
        if self.is_inside(x,y):
            return self.grid[y][x]
        return 'obstacle'