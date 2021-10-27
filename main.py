from game import Game
from queue import Queue, PriorityQueue
from util import Direction
from time import time

def uniform_cost_search(game: Game):
    print("Using uniform cost search:")
    move_queue = Queue()
    move_queue.put(game)
    dupes = set()
    while not move_queue.empty():
        new_game = move_queue.get()
        if new_game.check_solution():
            return new_game
        for dir in Direction:
            try:
                move_game = new_game.copy_move(dir)
                if move_game.string() not in dupes:
                    move_queue.put(move_game)
            except:
                pass

    print("ERROR: Unsolvable Puzzle")
    quit()


def misplaced_tile_search(game: Game):
    pass


def manhattan_search(game: Game):
    pass


if __name__=='__main__':
    # depth 0: 
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '\u25a1']], empty='\u25a1')

    # depth 1: uniform (0.001 seconds)
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '\u25a1', '8']], empty='\u25a1')

    # depth 2: uniform (0.002 seconds)
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['\u25a1', '7', '8']], empty='\u25a1')

    # depth 4: uniform (0.0171 seconds)
    game = Game([['1', '2', '3'], ['5', '\u25a1', '6'], ['4', '7', '8']], empty='\u25a1')

    # depth 8: uniform (0.665 seconds)
    # game = Game([['1', '3', '6'], ['5', '\u25a1', '2'], ['4', '7', '8']], empty='\u25a1')

    # depth 12: uniform (41.487 seconds)
    # game = Game([['1', '3', '6'], ['5', '\u25a1', '7'], ['4', '8', '2']], empty='\u25a1')

    # depth 16: uniform (Timeout)
    # game = Game([['1', '6', '7'], ['5', '\u25a1', '3'], ['4', '8', '2']], empty='\u25a1')

    # depth 20: uniform(Timeout)
    # game = Game([['7', '1', '2'], ['4', '8', '5'], ['6', '3', '\u25a1']], empty='\u25a1')

    # depth 24: uniform(Timeout)
    # game = Game([['0', '7', '2'], ['4', '6', '1'], ['3', '5', '8']], empty='\u25a1')

    
    start_time = time()
    x = uniform_cost_search(game)
    run_time = time() - start_time
    x.print_path()
    
    print(f"Took {run_time} seconds")

    