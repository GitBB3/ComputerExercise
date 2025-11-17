class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['empty' for _ in range(width)] for _ in range(height)] #all cells are initialized empty
        self.nest = [height // 2, width //2] #the "ant nest" is located at the middle of the given environment
        self.grid =[self.nest[0], self.nest[1]] #the grid of the nest is marked as such and not as "empty"