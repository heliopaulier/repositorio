import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve_path(filename: str):
    return os.path.join(BASE_PATH, "images", filename)
