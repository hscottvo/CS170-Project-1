from util import *
from copy import deepcopy


class Game:
    def __init__(self, start, empty): 
        self.start_state = start
        self.game_state = start
        self.empty = empty
        self.path = []
        self.coords = []
        self.__init_coords()
        self.size = len(start[0])
        self.solution = []
        self.__init_solution()
        self.max_val = self.size ** 2 - 1
       

    def __init_solution(self):
        for i in range(1, self.size+1):
            self.solution.append([str(j + self.size*(i-1)) for j in range(1, self.size+1)]) 
        self.solution[self.size-1][self.size-1] = self.empty 


    def __init_coords(self):
        for i in range(len(self.game_state)):
            for j in range(len(self.game_state)):
                if self.game_state[i][j] == self.empty:
                    self.coords = [i, j]

    
    def print(self, debug: bool = False): 
        for i in self.game_state:
            for j in i: 
                print(j + ' '*((self.max_val // 10 + 2) - len(j)), end='')
            print('')
        if debug: 
            print("Empty space is in: Row " + str(self.coords[0]), "Column " + str(self.coords[1]), sep='  ')

    
    def print_initial(self): 
        for i in self.start_state:
            for j in i: 
                print(j + ' '*((self.max_val // 10 + 2) - len(j)), end='')
            print('')
    

    def print_path(self):
        print('_' * 20)
        print("Starting State: " )
        self.print_initial()
        print('_' * 20)
        print("Current State: ")
        self.print()
        print('_' * 20)
        print("Path Taken (movement directions of the empty spot): ")
        print(self.path)
        print('_' * 20)


    def can_move(self, dir: Enum):
        return (dir == Direction.UP and self.coords[0] > 0) or (dir == Direction.DOWN and self.coords[0] < self.size - 1) or \
            (dir == Direction.LEFT and self.coords[1] > 0) or (dir == Direction.RIGHT and self.coords[1] < self.size - 1) 


    def move(self, dir: Enum):
        assert self.can_move(dir), "Invalid Operation: " + \
            dir.name + " when coordinates are: " + \
            str(self.coords) # denominator can't be 0
        self.__switch(self.coords, [sum(x) for x in zip(self.coords, dir.value)])


    def copy_move(self, dir:Enum):
        new_game = Game(self.__copy_string(), self.empty)
        new_game.move(dir)
        new_game.start_state = self.start_state
        new_game.path = self.path
        new_game.path.append(dir.name)
        return new_game


    def __switch(self, coords_a, coords_b):
        self.game_state[coords_a[0]][coords_a[1]], self.game_state[coords_b[0]][coords_b[1]] = \
            self.game_state[coords_b[0]][coords_b[1]], self.game_state[coords_a[0]][coords_a[1]]
        self.coords = coords_b
    

    def __copy_string(self):
        return [i.copy() for i in self.game_state]


    def manhattan_heuristic(self):
        ret = 0
        for i, row in enumerate(self.game_state):
            for j, item in enumerate(row):
                if item != self.empty:
                    curr_pos = (i, j)
                    item_num = int(item)
                    sol_pos = ((item_num-1)//self.size, (item_num-1)%self.size)
                    ret += manhattan_dist(sol_pos, curr_pos)
        return ret


    def misplaced_tile_hueristic(self):
        ret = 0
        for i, row in enumerate(self.game_state):
            for j, item in enumerate(row):
                if item != self.empty:
                    sol_val = i * self.size + j + 1
                    curr_val = int(item)
                    if sol_val != curr_val:
                        ret += 1
        return ret


    def string(self):
        return ' '.join([i for i in [' '.join(j) for j in self.game_state]])


    def check_solution(self):
        return self.game_state == self.solution



if __name__ == "__main__": 
    empty_char = '\u25a1'
    user_input = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', empty_char]]
    x = Game(user_input, empty_char)
    # y = x.game_state.deepcopy()
    x.move(Direction.LEFT)
    x.move(Direction.LEFT)
    y = x.copy_move(Direction.RIGHT)
    z = y.copy_move(Direction.UP)
    z.print_path()

    