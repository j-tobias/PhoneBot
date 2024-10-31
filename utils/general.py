import os
import json




def load_key(name:str):

    with open("APIKEY.json", "r") as f:
        keys = json.load(f)
    
    return keys[name]

