import requests
import json


def getkey (name:str="VAPI PRIVATE")-> str:
    with open("APIKEY.json", "r") as f:
        keys = json.load(f)
    return keys[name]

def getAssistants():
    url = "https://api.vapi.ai/assistant"
    
    headers = {
        "Authorization": f"Bearer {getkey()}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        assistants = response.json()
        return assistants
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def updateAssistant(assistant_id: str, update_data: dict) -> dict:
    url = f"https://api.vapi.ai/assistant/{assistant_id}"
    
    headers = {
        "Authorization": f"Bearer {getkey()}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        updated_assistant = response.json()
        return updated_assistant
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def updateSystemMessage(id:str, systemmessage:str)->dict:

    print("ID: ", id)
    print("SysMsg: ", systemmessage)

    id = str(id)
    systemmessage = str(systemmessage)

    payload = {"model":{
        "provider":"openai",
        "model":"gpt-4o-mini",
        "messages":[
            {"role":"system","content":systemmessage}
        ]
    }}

    response = updateAssistant(id, payload)

    return response



ID = "82b64b97-8e14-436c-88fe-c8581c8a2591"
