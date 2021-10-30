from game import Game
from queue import Queue, PriorityQueue
from util import Direction, PrioGame, Searches
from time import time
from random import randint
import json
import os

timeout_time = 1000
direction_enum = list(Direction)
search_names = ["Uniform Cost Search", "Misplaced A-Star", "Manhattan A-Star"]


def random_puzzle(size: int, empty: str, moves: int) -> Game:
    solution = []
    for i in range(1, size+1):
        solution.append([str(j + size*(i-1)) for j in range(1, size+1)]) 
    solution[size-1][size-1] = empty 
    ret = Game(solution, empty)
    for i in range(moves):
        try:
            ret.move(direction_enum[randint(0, 3)])
        except: 
            pass
    return ret


def uniform_cost_search(game: Game):
    start_time = time()
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


def average_time(game: Game, times: dict, depth: int) -> None:
    print(f'With depth {depth}: ')
    time_list_uniform = []
    time_list_tile = []
    time_list_manhattan = []
    for i in range(0, 10):
        start_time = time()
        uniform_cost_search(game)
        time_list_uniform.append(time() - start_time)

        start_time = time()
        misplaced_tile_search(game)
        time_list_tile.append(time() - start_time)

        start_time = time()
        manhattan_search(game)
        time_list_manhattan.append(time() - start_time)
    times[f'depth {depth}'] = {}
    times[f'depth {depth}']['uniform depth'] = ' '.join([str(round(sum(time_list_uniform)/len(time_list_uniform), 3)), 'seconds'])
    times[f'depth {depth}']['misplaced tile'] = ' '.join([str(round(sum(time_list_tile)/len(time_list_tile), 3)), 'seconds'])
    times[f'depth {depth}']['manhattan distance'] = ' '.join([str(round(sum(time_list_manhattan)/len(time_list_manhattan), 3)), 'seconds'])


def log_times():
    times = {}

    depth = 0
    game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '\u25a1']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 1
    game = Game([['1', '2', '3'], ['4', '5', '6'], ['7', '\u25a1', '8']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 2
    game = Game([['1', '2', '3'], ['4', '5', '6'], ['\u25a1', '7', '8']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 4
    game = Game([['1', '2', '3'], ['5', '\u25a1', '6'], ['4', '7', '8']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 8
    game = Game([['1', '3', '6'], ['5', '\u25a1', '2'], ['4', '7', '8']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 12
    game = Game([['1', '3', '6'], ['5', '\u25a1', '7'], ['4', '8', '2']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 16
    game = Game([['1', '6', '7'], ['5', '\u25a1', '3'], ['4', '8', '2']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 20
    game = Game([['7', '1', '2'], ['4', '8', '5'], ['6', '3', '\u25a1']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 24
    game = Game([['\u25a1', '7', '2'], ['4', '6', '1'], ['3', '5', '8']], empty='\u25a1')
    average_time(game, times, depth)

    depth = 31
    game = Game([['6', '4', '7'], ['8', '5', '\u25a1'], ['3', '2', '1']], empty = '\u25a1')
    average_time(game, times, depth)

    
    print(json.dumps(times, indent=4))
    with open('search_logs.json', 'w') as outfile:
        json.dump(times, outfile, indent=4)
    

def run_input_game(empty, search):
    with open('input.txt') as f:
        lines = f.readlines()
    new_lines = []
    for i in lines:
        new_lines.append(i.replace('0', empty).rstrip('\n').split())
    
    game = Game(new_lines, empty)
    if search.value == 0:
        print("With Uniform-Cost Search:")
        # uniform
        start = time()
        new_game = uniform_cost_search(game)
        new_game.print_path()
        print(f"Took {round(time() - start, 3)} seconds")
    elif search.value == 1:
        print("With Misplaced Tile A-Star:")
        # misplaced
        start = time()
        new_game = misplaced_tile_search(game)
        new_game.print_path()
        print(f"Took {round(time() - start, 3)} seconds")
    elif search.value == 2:
        print("With Manhattan Distance A-Star")
        start = time()
        new_game = manhattan_search(game)
        new_game.print_path()
        print(f"Took {round(time() - start, 3)} seconds")
    else:
        print("Invalid Search Value")
        quit()


if __name__=='__main__':

    # log_times() 
    run_input_game('\u25a1', Searches.manhattan)
    # game = Game([['\u25a1', '7', '2'], ['4', '6', '1'], ['3', '5', '8']], empty='\u25a1')   
    # solved_game = manhattan_search(game)
    # solved_game.print_path()
    


    