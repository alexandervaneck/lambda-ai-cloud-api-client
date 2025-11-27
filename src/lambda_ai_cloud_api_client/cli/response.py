import json


def print_json(d: dict | list) -> None:
    print(json.dumps(d, indent=2))
