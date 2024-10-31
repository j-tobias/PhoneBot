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



@app.get("/ping")
async def root():
    return {"response": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)