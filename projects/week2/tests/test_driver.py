import json

import pytest

from driver import bfs_search, dfs_search, A_star_search


def test_bfs(bfs_sample):
    result = bfs_search(bfs_sample[0])
    assert result == bfs_sample[1]


def test_dfs(dfs_sample):
    result = dfs_search(dfs_sample[0])
    assert result == dfs_sample[1]


def test_ast(ast_sample):
    result = A_star_search(ast_sample[0])
    assert result == ast_sample[1]

