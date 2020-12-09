import json
import math
import os

import pytest

from driver import PuzzleState

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(params=
    [
        (
            PuzzleState((1,2,5,3,4,0,6,7,8), 3),
            {
                'path_to_goal': ['Up', 'Left', 'Left'], 
                'nodes_expanded': 10, 
                'cost_of_path': 3, 
                'search_depth': 3, 
                'max_search_depth': 4
            }
        ),
       (
           PuzzleState((6,1,8,4,0,2,7,3,5), 3),
           {
               'path_to_goal': ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up'],
               'cost_of_path': 20,
               'nodes_expanded': 54094,
               'search_depth': 20,
               'max_search_depth': 21,
           }
       ),
       (
           PuzzleState((8,6,4,2,1,3,5,7,0), 3),
           {
               'path_to_goal': ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left'],
               'cost_of_path': 26,
               'nodes_expanded': 166786,
               'search_depth': 26,
               'max_search_depth': 27,
           }
       ),
  ]
)
def bfs_sample(request):
  return request.param



with open(os.path.join(FILE_PATH, "resources", "dfs_result_1.json"), "r") as fp:
    dfs_result_1 = json.load(fp)

with open(os.path.join(FILE_PATH, "resources", "dfs_result_2.json"), "r") as fp:
    dfs_result_2 = json.load(fp)

with open(os.path.join(FILE_PATH, "resources", "dfs_result_3.json"), "r") as fp:
    dfs_result_3 = json.load(fp)

@pytest.fixture(params=
    [
        (PuzzleState((1,2,5,3,4,0,6,7,8), 3), dfs_result_1),
        (PuzzleState((6,1,8,4,0,2,7,3,5), 3), dfs_result_2),
        (PuzzleState((8,6,4,2,1,3,5,7,0), 3), dfs_result_3)
    ]
)
def dfs_sample(request):
  return request.param


@pytest.fixture(params=
    [
        (
            PuzzleState((6,1,8,4,0,2,7,3,5), 3),
            {
                "path_to_goal": ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up'],
                "cost_of_path": 20,
                "nodes_expanded": 651,
                "search_depth": 20,
                "max_search_depth": 20
            }
        ),
        (
            PuzzleState((8,6,4,2,1,3,5,7,0), 3), 
            {
                'path_to_goal': ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left'],
                'cost_of_path': 26,
                'nodes_expanded': 583,
                'search_depth': 26,
                'max_search_depth': 26
            }
        )
    ]
)
def ast_sample(request):
  return request.param
