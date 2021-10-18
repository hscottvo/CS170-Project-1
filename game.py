from enum import Enum

class Direction(Enum): 
    DOWN = (1, 0)
    UP = (-1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


class Game:
    def __init__(self, start): 
        self.game_state = start
        self.coords = [-1, -1]
        for i in range(len(start)):
            for j in range(len(start)):
                if start[i][j] == '\u25a1':
                    self.coords = [i, j]
        self.size = len(start[0])
        # self.solution = [str(i) for i in range(1, self.size+1)]
        self.solution = []
        self.__init_solution()
       

    def __init_solution(self):
        for i in range(1, self.size+1):
            self.solution.append([str(j + self.size*(i-1)) for j in range(1, self.size+1)]) 
        self.solution[self.size-1][self.size-1] = '\u25a1'  

    
    def print(self, debug: bool = False): 
        for i in self.game_state:
            print(i[0], i[1], i[2], sep=' ', end='\n')
        print('')
        if debug: 
            print("Empty space is in: Row " + str(self.coords[0]), "Column " + str(self.coords[1]), sep='  ')
    

    def can_move(self, dir: Enum):
        return (dir == Direction.UP and self.coords[0] > 0) or (dir == Direction.DOWN and self.coords[0] < self.size - 1) or \
            (dir == Direction.LEFT and self.coords[1] > 0) or (dir == Direction.RIGHT and self.coords[1] < self.size - 1) 


    def move(self, dir: Enum):
        assert self.can_move(dir), "Invalid Operation: " + \
            dir.name + " when coordinates are: " + \
            str(self.coords) # denominator can't be 0
        self.__switch(self.coords, [sum(x) for x in zip(self.coords, dir.value)])
        pass

    def __switch(self, coords_a, coords_b):
        self.game_state[coords_a[0]][coords_a[1]], self.game_state[coords_b[0]][coords_b[1]] = \
            self.game_state[coords_b[0]][coords_b[1]], self.game_state[coords_a[0]][coords_a[1]]
        self.coords = coords_b


    def check_solution(self):
        return self.game_state == self.solution


if __name__ == "__main__": 
    user_input = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '\u25a1', '11', '12'], ['13', '14', '15', '16']]
    x = Game(user_input)
    x.print()
    x.move(Direction.LEFT)
    x.print()
    x.move(Direction.UP)
    x.print()
    print(x.check_solution())
    print(x.solution)
    print(x.game_state)
    