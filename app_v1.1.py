import json
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import asyncio
from utils import computeMetrics, loadBasicDF, getReport
from vapi import updateSystemMessage, getAssistants


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



with gr.Blocks() as app:


    gr.HTML("""
    <head>
        <meta charset="UTF-8">
        <style>h1 {text-align: center;}</style>
    </head>
    <body><h1>PhoneBot 📞</h1></body>""")

    with gr.Tab("+49 176 362209833"):

        # SYSTEM VARIABLES
        AssistantID = gr.Textbox(value="82b64b97-8e14-436c-88fe-c8581c8a2591", render=True, label="AssistantID", interactive=False)

        gr.Markdown("## Overview")

        SystemMessage = gr.Textbox(value=loadAssistant("82b64b97-8e14-436c-88fe-c8581c8a2591"), lines=10, placeholder="Please write the System Prompt here", container=False, label=None)

        updatebtn = gr.Button("update")

        response = gr.Textbox(label="Server Response")

        updatebtn.click(updateSystemMessage, inputs=[AssistantID, SystemMessage], outputs=[response], preprocess=False)

app.launch()
