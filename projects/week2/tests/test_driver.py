import json

import pytest

from driver import bfs_search, dfs_search


@pytest.mark.skip()
def test_bfs(bfs_sample):
    result = bfs_search(bfs_sample[0])
    assert result == bfs_sample[1]


state = 1

def test_dfs(dfs_sample):
    global state
    result = dfs_search(dfs_sample[0])
    with open(f"dfs_result_{state}.json", "w") as fp:
        json.dump(result, fp)
    state +=1
    assert result == dfs_sample[1]

