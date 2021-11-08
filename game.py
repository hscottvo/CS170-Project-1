from util import *


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
        '''Calculates the solution of the puzzle. Returns None'''
        for i in range(1, self.size+1):
            self.solution.append([str(j + self.size*(i-1)) for j in range(1, self.size+1)]) 
        self.solution[self.size-1][self.size-1] = self.empty 


    def __init_coords(self):
        '''Calculates coordinates of empty tile. Returns None'''
        for i in range(len(self.game_state)):
            for j in range(len(self.game_state)):
                if self.game_state[i][j] == self.empty:
                    self.coords = [i, j]

    
    def print(self, debug: bool = False): 
        '''Prints formatted game object. Returns None
        If debug is true, then print coordinate of empty space'''
        for i in self.game_state:
            for j in i: 
                print(j + ' '*((self.max_val // 10 + 2) - len(j)), end='')
            print('')
        if debug: 
            print("Empty space is in: Row " + str(self.coords[0]), "Column " + str(self.coords[1]), sep='  ')

    
    def print_initial(self): 
        '''Prints the starting state of the game. Returns None'''
        for i in self.start_state:
            for j in i: 
                print(j + ' '*((self.max_val // 10 + 2) - len(j)), end='')
            print('')
    

    def print_path(self):
        '''Prints path taken from starting state to current state. Returns None'''
        print('_' * 20)
        print("Starting State: " )
        self.print_initial()
        print('_' * 20)
        print("Current State: ")
        self.print()
        print('_' * 20)
        print("Path Taken (movement directions of the empty spot): ")
        print(self.path)
        print(f'{len(self.path)} move(s)')
        print('_' * 20)


    def can_move(self, dir: Enum):
        '''Takes in a direction. Returns a bool.
        Calculates if the input move is valid in the game'''
        return (dir == Direction.UP and self.coords[0] > 0) or (dir == Direction.DOWN and self.coords[0] < self.size - 1) or \
            (dir == Direction.LEFT and self.coords[1] > 0) or (dir == Direction.RIGHT and self.coords[1] < self.size - 1) 


    def move(self, dir: Enum):
        '''Takes in a direction. Returns None
        Mutates game state to specified direction'''
        assert self.can_move(dir), "Invalid Operation: " + \
            dir.name + " when coordinates are: " + \
            str(self.coords) # denominator can't be 0
        self.__switch(self.coords, [sum(x) for x in zip(self.coords, dir.value)])


    def copy_move(self, dir:Enum):
        '''Takes in a direction. Returns a game object with the mutated state'''
        new_game = Game(self.__copy_string(), self.empty)
        new_game.move(dir)
        new_game.start_state = self.start_state
        new_game.path = (self.path).copy()
        new_game.path.append(dir.name)
        return new_game


    def __switch(self, coords_a, coords_b):
        '''Takes in two strings. Returns None
        Swaps the positions of two coordinates. Resets the coordinates of the missing tile accordingly'''
        self.game_state[coords_a[0]][coords_a[1]], self.game_state[coords_b[0]][coords_b[1]] = \
            self.game_state[coords_b[0]][coords_b[1]], self.game_state[coords_a[0]][coords_a[1]]
        self.coords = coords_b
    

    # https://docs.python.org/3/library/copy.html
    def __copy_string(self):
        '''Takes in None. Returns string
        Stringified version of the game state, used for hashing the set of previously-visited states'''
        return [i.copy() for i in self.game_state]


    def manhattan_heuristic(self):
        '''Takes in None. Returns int
        Calculates manhattan f(x) = len(self.path) + total manhattan distances across tiles'''
        ret = 0
        for i, row in enumerate(self.game_state):
            for j, item in enumerate(row):
                if item != self.empty:
                    curr_pos = (i, j)
                    item_num = int(item)
                    sol_pos = ((item_num-1)//self.size, (item_num-1)%self.size)
                    ret += manhattan_dist(sol_pos, curr_pos)
        return ret + len(self.path)


    def misplaced_tile_heuristic(self):
        '''Takes in None. Returns int
        Calculates misplaced tile heuristic f(x) = len(self.path) + number of tiles in non-final positions'''
        ret = 0
        for i, row in enumerate(self.game_state):
            for j, item in enumerate(row):
                if item != self.empty:
                    sol_val = i * self.size + j + 1
                    curr_val = int(item)
                    if sol_val != curr_val:
                        ret += 1
        return ret + len(self.path)


    def string(self):
        '''Takes in None. Returns string
        Stringified version of game state'''
        return ' '.join([i for i in [' '.join(j) for j in self.game_state]])


    def check_solution(self):
        '''Takes in None. Returns bool
        return true if game is solved'''
        return self.game_state == self.solution



if __name__ == "__main__": 
    empty_char = '\u25a1'
    user_input = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', empty_char, '15']]
    x = Game(user_input, empty_char)
    # y = x.game_state.deepcopy()
    x.print()
    print(x.string())
    print(x.check_solution())
    print(x.manhattan_heuristic())




