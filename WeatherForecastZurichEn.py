import json
import os
import smtplib
import requests
from google import genai
from google.genai import types
from email.message import EmailMessage


PARAMS_OWM = {
    "appid" : os.environ.get("APPID"),
    "lat": 47.376696,
    "lon": 8.558962,
    "units" : "metric",
    "cnt" : 5,
}

PARAMS_GEM = {
    "gemini_api_key" : os.environ.get("GEMINI_API_KEY"),
}

RECIPIENT1 = os.environ.get("RECIPIENT1")
RECIPIENT2 = os.environ.get("RECIPIENT2")

#with requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS_OWM) as api_response:
  #with open ("response.json", "w") as weather_file:
    #json.dump(api_response.json(), weather_file, indent=4)
response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS_OWM)
weather_data = response.json()
description = response.json()["list"][0]["weather"][0]["description"]
prompt = (f"Use weather data available in {weather_data} and generate a short clothing recommendation in html format."
          f"generate recommendation only for the same date this prompt is being sent over."
          f"output HTML markup (<p>, <ul>, <li>, <strong>, etc.) to avoid markdown code blocks like ```html."
          f"be short, concise, clear and to the point with your recommendations and generate a funny graphic that mirros the forecast sentiments."
          f"embed that graphic into the html reponse to improve the visuals of the message.")
# client = genai.Client(api_key=PARAMS_GEM["gemini_api_key"])
client = genai.Client(
    api_key= PARAMS_GEM["gemini_api_key"],
    http_options= types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            initial_delay=2,
            attempts=3,
            backoff_factor=2,
            http_status_forcelist=[429, 500, 502, 503, 504],
        )
    ),
)
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input= prompt
)
completion = interaction.output_text
print(completion)

sender_email = os.environ.get("EMAIL")
app_password = os.environ.get("PASSWORD")
recipients = [RECIPIENT1, RECIPIENT2]

gemini_response = completion

msg = EmailMessage()
msg["Subject"] =  f"Today's Weather Forecast🌤️ | {description}"
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
