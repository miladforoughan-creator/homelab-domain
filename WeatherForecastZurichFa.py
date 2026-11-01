import json
import os
import smtplib
import requests
from google import genai
from email.message import EmailMessage


PARAMS = {
    "appid" : os.environ.get("APPID"),
    "lat": 47.376696,
    "lon": 8.558962,
    "units" : "metric",
    "cnt" : 5,
    "gemini_api_key" : os.environ.get("GEMINI_API_KEY"),
}

RECIPIENT1 = os.environ.get("RECIPIENT1")
RECIPIENT2 = os.environ.get("RECIPIENT2")
gemini_input = os.environ.get("GEMENI_INPUT")

#with requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS) as api_response:
  #with open ("response.json", "w") as weather_file:
    #json.dump(api_response.json(), weather_file, indent=4)
response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS)
weather_data = response.json()
description = response.json()["list"][0]["weather"][0]["description"]

prompt = gemini_input
client = genai.Client(api_key= PARAMS["gemini_api_key"])
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input= prompt
)
completion = interaction.output_text
print(interaction.output_text)

sender_email = os.environ.get("EMAIL")
app_password = os.environ.get("PASSWORD")
recipients = [RECIPIENT1, RECIPIENT2]

gemini_response = completion

msg = EmailMessage()
msg["Subject"] =  f"پیش‌بینی هوا با مامان پوری🌤️ | {description}"
msg["From"] = sender_email
msg["To"] = recipients
msg.set_content(gemini_response, subtype="html")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
    print("Email sent successfully with special characters!")
except Exception as e:
    print(f"An error occurred: {e}")


