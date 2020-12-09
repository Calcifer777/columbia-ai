"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
"""

import copy
from collections import deque
import logging
import queue as Q
from queue import PriorityQueue
import time
import resource
import sys
import math

logger = logging.getLogger()
logger.setLevel(logging.WARN)

# The Class that Represents the Puzzle


class PuzzleState(object):
    """docstring for PuzzleState"""
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        self.path = None
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break
        self.goal = tuple(range(len(self.config)))
        assert len(self.goal) == len(self.config)

    def __repr__(self):
        s = "\n"
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            s += str(line)+"\n"
        return s

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.config == other.config

    def __lt__(self, other):
        return (
            self.cost + calculate_total_cost(self) <= 
            other.cost + calculate_total_cost(other)
        )

    def __hash__(self):
        return hash(str(self.config))

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) != 0:
            return self.children
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()
        ]
        self.children = list(filter(None, children))
        return self.children

    def is_goal(self):
        return self.config == self.goal

    def get_path(self):
        if self.path:
            return self.path
        state = self
        path = []
        while state.parent is not None:
            path.append(state.action)
            state = state.parent
        self.path = path[::-1]
        return self.path

# Function that Writes to output.txt
# Students need to change the method to have the corresponding
# parameters

def writeOutput():
    # Student Code Goes here
    pass


def bfs_search(initial_state):
    """BFS search"""
    q = Q.Queue()
    q.put(initial_state)
    nodes_expanded = set()
    max_search_depth = 0
    while q.empty() is False:
        state = q.get()
        if state.is_goal():
            break
        for new_state in state.expand():
            if new_state not in nodes_expanded:
                q.put(new_state)
                if new_state.cost > max_search_depth:
                    max_search_depth = new_state.cost
        nodes_expanded.add(state)
        logging.info(f"Queue size: {q.qsize()}")
        logging.info(f"Visited: {len(nodes_expanded)}")
        logging.info(state)
    result = {
        'path_to_goal': state.get_path(),
        'nodes_expanded': len(nodes_expanded),
        'cost_of_path': state.cost,
        'search_depth': len(state.get_path()),
        'max_search_depth': max_search_depth
    }
    return result


def dfs_search(initial_state):
    """DFS search"""
    q = Q.LifoQueue()
    q.put(initial_state)
    nodes_visited, nodes_expanded = set(), set()
    nodes_visited.add(initial_state)
    max_search_depth = 0
    while q.empty() is False:
        state = q.get()
        if state.is_goal():
            break
        for new_state in state.expand()[::-1]:
            if new_state not in nodes_visited:
                q.put(new_state)
                nodes_visited.add(new_state)
                if new_state.cost > max_search_depth:
                    max_search_depth = new_state.cost
        nodes_expanded.add(state)
        logging.info(f"Queue size: {q.qsize()}")
        logging.info(f"Visited: {len(nodes_expanded)}")
    result = {
        'path_to_goal': state.get_path(),
        'nodes_expanded': len(nodes_expanded),
        'cost_of_path': state.cost,
        'search_depth': len(state.get_path()),
        'max_search_depth': max_search_depth
    }
    return result


def A_star_search(initial_state):
    """A * search"""
    q = PriorityQueue()
    q.put((calculate_total_cost(initial_state), initial_state))
    visited = set()
    nodes_expanded = set()
    visited = set()
    frontier = set()
    frontier.add(initial_state)
    max_search_depth = 0
    while q.empty() is False:
        state_cost, state = q.get()
        visited.add(state)
        frontier.remove(state)
        if state.is_goal():
            break
        for new_state in state.expand():
            if new_state not in (nodes_expanded | frontier):
                q.put((calculate_total_cost(new_state), new_state))
                frontier.add(new_state)
                visited.add(new_state)
            elif new_state in frontier:

                if new_state.cost > max_search_depth:
                    max_search_depth = new_state.cost
        nodes_expanded.add(state)
        logging.info(f"Queue size: {q.qsize()}")
        logging.info(f"Visited: {len(visited)}")
        logging.info(state)
    result = {
        'path_to_goal': state.get_path(),
        'nodes_expanded': len(nodes_expanded),
        'cost_of_path': state.cost,
        'search_depth': len(state.get_path()),
        'max_search_depth': max_search_depth
    }
    return result


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    h_cost = 0
    for idx, value in enumerate(state.config):
        h_cost += calculate_manhattan_dist(idx, value, state.n)
    return state.cost + h_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    if value == 0:
        return 0
    value_x, value_y = idx // n, idx % n
    sol_x, sol_y = value // n, value % n
    return abs(sol_x-value_x) + abs(sol_y-value_y)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    puzzle_state.is_goal()


# Main Function that reads in Input and Runs 
# corresponding Algorithm
def main():
    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    if sm == "bfs":
        result = bfs_search(hard_state)
    elif sm == "dfs":
        result = dfs_search(hard_state)
    elif sm == "ast":
        result = A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")
    print(result)
    return


if __name__ == '__main__':
    main()
