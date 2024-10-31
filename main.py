from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from mailjet_rest import Client
import uvicorn
import json
import os


# Set up the app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Credentials
MAILJET_KEY = os.getenv("MAILJET_KEY")
MAILJET_SECRET = os.getenv("MAILJET_SECRET")


# ENDPOINT FOR VAPI POSTS
@app.post("/")
async def root(request: Request):
    body = await request.json()
    if body["message"]["type"] == "end-of-call-report":

        # Initiate variables for the Email
        summary         = ""
        timestamp       = ""
        customer        = ""
        called_number   = ""
        escalation      = ""
        transcript      = ""
        recording       = ""

        replacements = [summary, timestamp, customer, called_number, escalation, transcript, recording]

        # Read the End-of-Call-Report
        try:
            body = body["message"]
            summary = body["analysis"]["summary"]
            timestamp = body["timestamp"]
            transcript = body["transcript"]
            recording = body["stereoRecordingUrl"]
            customer = body["customer"]["number"]
            called_number = body["phoneNumber"]["number"]
            escalation = body["analysis"]["successEvaluation"]

            name = str(timestamp)
            name = name.replace("-","")
            name = name.replace(":","")
            name = name.replace(".","")
        except Exception as e:
            return HTTPException(status_code=400, detail=f"End of Call Report not in correct format: {e}")
        
        # Try to save the Report
        # try:
        #     with open(f"Logs/Reports/{name}.json", mode="w") as f:
        #         json.dump(body, f, indent=4)
        # except:
        #     pass

        # Load the Email Template
        with open('EmailTemplate.html', 'r') as file:
            template = file.read()
        
        olds = [
            "#summary#",
            "#timestamp#",
            "#customer#",
            "#called_number#",
            "#escalation#",
            "#transcript#",
            "#recording#"]
        
        # Attempt to replace the placeholders
        for replacement, old in zip(replacements, olds):
            try:
                template = template.replace(old, replacement)
            except:
                template = template.replace(old, "Error")


        subject = f'Report - escalation: ?'

        mailjet = Client(auth=(MAILJET_KEY, MAILJET_SECRET), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "justus.tobias@googlemail.com",
                "Name": "PhoneBot"
            },
            "To": [
                {
                "Email": "sprachbot@visana-pflege.de",
                "Name": "Visana"
                }
            ],
            "Subject": f"{subject}",
            "TextPart": "",
            "HTMLPart": f"{template}",
            }
        ]
        }
        result = mailjet.send.create(data=data)
        print("Email Send Response: ",result)


# ENDPOINT FOR CHECKING AVAILABILITY
@app.get("/ping")
async def root():
    return {"response": "Hello World"}


import gradio as gr
from utils.app import loadAssistant, updateSystemMessage


with gr.Blocks() as demo:

    gr.HTML("""
    <head>
        <meta charset="UTF-8">
        <style>h1 {text-align: center;}</style>
    </head>
    <body><h1>PhoneBot 📞</h1></body>""")

    with gr.Tab("+49 (821) 90579038"):

        # TAB VARIABLES
        ASSISTANT_ID_1 = "82b64b97-8e14-436c-88fe-c8581c8a2591"

        gr.Markdown("## Overview")

        gr.Markdown("### You can use different variables in the SystemMessage to give the Agent extra information")
        gr.Markdown(" - {{now}} Current date and time (UTC) (Jan 1, 2024 12:00 PM)")
        gr.Markdown(" - {{date}} Current data (UTC) (Jan 1, 2024)")
        gr.Markdown(" - {{time}} Current time (UTC) (12:00 PM)")
        gr.Markdown(" - {{month}} Current month (UTC) (January)")
        gr.Markdown(" - {{day}} Current day of month (UTC) (1)")
        gr.Markdown(' - {{"now" | date: "%A, %b %d, %Y, %I:%M %p", "Europe/Berlin"}} For the full Time with Day of the Week (Thursday, Oct 31, 2024, 06:45 PM)')

        SystemMessage = gr.Textbox(value=loadAssistant(ASSISTANT_ID_1), lines=10, placeholder="Please write the System Prompt here", container=False, label=None)

        with gr.Row():

            with gr.Column(scale=7):
                updatebtn = gr.Button("update")
            with gr.Column(scale=1):
                refreshbtn = gr.Button("🔄 refresh")

        response = gr.Textbox(label="Server Response")

        refreshbtn.click(lambda: loadAssistant(ASSISTANT_ID_1), outputs=[SystemMessage], preprocess=False)
        updatebtn.click(lambda SysMsg:updateSystemMessage(ASSISTANT_ID_1, SysMsg), inputs=[SystemMessage], outputs=[response], preprocess=False)


app = gr.mount_gradio_app(app, demo, path="/app")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)