from game import Game
from queue import Queue, PriorityQueue
from heapq import heapify, heappush, heappop
from util import Direction, PrioGame
from time import time

timeout_time = 5


def uniform_cost_search(game: Game):
    start_time = time()
    print("Using uniform cost search:")
    move_queue = Queue()
    move_queue.put(game)
    dupes = {game.string()}
    while not move_queue.empty():
        new_game = move_queue.get()
        if new_game.check_solution():
            return new_game
        for dir in Direction:
            try:
                move_game = new_game.copy_move(dir)
                if move_game.string() not in dupes:
                    move_queue.put(move_game)
                    dupes.add(move_game.string())
            except:
                pass
        if time() - start_time > timeout_time:
            print(f"TIMEOUT: {timeout_time} seconds")
            quit()

    print("ERROR: Unsolvable Puzzle")
    quit()


def misplaced_tile_search(game: Game):
    print("Using misplaced tile A-star:")
    start_time = time()
    move_queue = PriorityQueue()
    move_queue.put(PrioGame(game.misplaced_tile_heuristic(), game))
    dupes = {game.string()}
    while not move_queue.empty():
        prio_game = move_queue.get()
        new_game = prio_game.item
        if new_game.check_solution():
            return new_game
        for dir in Direction:
            try:
                move_game = new_game.copy_move(dir)
                if move_game.string() not in dupes:
                    move_queue.put(PrioGame(move_game.misplaced_tile_heuristic(), move_game))
                    dupes.add(move_game.string())
            except:
                pass
        if time() - start_time > timeout_time:
                print(f"TIMEOUT: {timeout_time} seconds")
                quit()
    print("ERROR: Unsolvable Puzzle")
    quit()
  

def manhattan_search(game: Game):
    print("Using Manhattan Distance A-star:")
    start_time = time()
    move_queue = PriorityQueue()
    move_queue.put(PrioGame(game.manhattan_heuristic(), game))
    dupes = {game.string()}
    while not move_queue.empty():
        prio_game = move_queue.get()
        new_game = prio_game.item
        if new_game.check_solution():
            return new_game
        for dir in Direction:
            try:
                move_game = new_game.copy_move(dir)
                if move_game.string() not in dupes:
                    move_queue.put(PrioGame(move_game.manhattan_heuristic(), move_game))
                    dupes.add(move_game.string())
            except:
                pass
        if time() - start_time > timeout_time:
            print(f"TIMEOUT: {timeout_time} seconds")
            quit()
    print("ERROR: Unsolvable Puzzle")
    quit()


if __name__=='__main__':

    # depth 0: uniform (0.0003 seconds)
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '\u25a1']], empty='\u25a1')

    # depth 1: uniform (0.001 seconds)
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '\u25a1', '8']], empty='\u25a1')

    # depth 2: uniform (0.007 seconds)
    # game = Game([['1', '2', '3'], ['4', '5', '6'], ['\u25a1', '7', '8']], empty='\u25a1')

    # depth 4: uniform (0.011 seconds)
    # game = Game([['1', '2', '3'], ['5', '\u25a1', '6'], ['4', '7', '8']], empty='\u25a1')

    # depth 8: uniform (0.051 seconds)
    # game = Game([['1', '3', '6'], ['5', '\u25a1', '2'], ['4', '7', '8']], empty='\u25a1')

    # depth 12: uniform (0.402 seconds)
    # game = Game([['1', '3', '6'], ['5', '\u25a1', '7'], ['4', '8', '2']], empty='\u25a1')

    # depth 16: uniform (2.66 seconds)
    # game = Game([['1', '6', '7'], ['5', '\u25a1', '3'], ['4', '8', '2']], empty='\u25a1')

    # depth 20: uniform(3.705 seconds)
    # game = Game([['7', '1', '2'], ['4', '8', '5'], ['6', '3', '\u25a1']], empty='\u25a1')

    # depth 24: uniform(17.388 seconds)
    game = Game([['\u25a1', '7', '2'], ['4', '6', '1'], ['3', '5', '8']], empty='\u25a1')

    
    start_time = time()
    solved_game = uniform_cost_search(game)
    p1 = Process(target=uniform_cost_search, args=(game,))
    p1.start()

    # solved_game = misplaced_tile_search(game)
    # solved_game = manhattan_search(game)
    run_time = time() - start_time
    solved_game.print_path()
    
    print(f"Took {run_time} seconds")


    