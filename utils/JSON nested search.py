import json
import warnings
from importlib import import_module
import os.path as osp
from pathlib import Path

from tqdm import tqdm


def json_extract(obj, key):
    """
    Extract nested values from a JSON tree.
    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)

    if len(values) == 1:
        return values[0]
    else:
        return values
