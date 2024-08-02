import toml
from typing import List

def load_config(name: List[str]):
    with open('src/pyproject.toml', 'r') as f:
        config = toml.load(f)
    if len(name) > 1:
        return config[name[0]][name[1]]
    else:
        return config[name[0]]
    

