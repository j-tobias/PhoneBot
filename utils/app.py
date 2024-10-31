import json

from .vapi import updateSystemMessage, getAssistants



def loadconfig()-> list:

    with open("config.json", "r") as f:
        config = json.load(f)
    
    numbers = config["numbers"]

    return numbers

def getnumber(number:str)-> dict:

    assistants = loadconfig()

    for assistant in assistants:
        if assistant["number"] == number:
            return assistant
        
    return None

def savetoconfig(number:str, key:str, value):
    assistants = loadconfig()

    # having a list in the config is a bad idea i have to change that
    return None

def loadAssistant(id:str):

    assistants = getAssistants()

    with open("Assistants.json", "w") as f:
        json.dump(assistants, f, indent=4)
    
    for assistant in assistants:
        if assistant["id"] == id:
            Assistant = assistant

    SystemMessage = Assistant["model"]["messages"][0]["content"]
    
    return SystemMessage