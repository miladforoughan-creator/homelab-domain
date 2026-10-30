import json
import os
import smtplib
import requests
from google import genai
from email.message import EmailMessage


PARAMS = {
  "openweathermap": {
    "appid" : os.environ.get("APPID"),
    "lat": 47.376696,
    "lon": 8.558962,
    "units" : "metric",
    "cnt" : 5},
    "gemini_api_key" : os.environ.get("gemini_api_key"),
}


#with requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS["openweathermap"]) as api_response:
  #with open ("response.json", "w") as weather_file:
    #json.dump(api_response.json(), weather_file, indent=4)
response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=PARAMS)
weather_data = response.json()
prompt = (f"Use weather data available in {weather_data} and generate a short clothing recommendation in Gilaki (Rashti) dialect and html format. "
          f"the response.json file includes 5-day forecast. generate recommendation only "
          f"for the same date this prompt is being sent over. Use Farsi language and RTL format to generate the html response. "
          f"output HTML markup (<p>, <ul>, <li>, <strong>, etc.) to avoid markdown code blocks like ```html."
          f" use TiVasee Youtube channel character Maman Poori مامان پوری to carry the expressions suiting the forecast sentiment.")

client = genai.Client(api_key= PARAMS["gemini_api_key"])
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input= prompt
)
completion = interaction.output_text
print(interaction.output_text)

sender_email = os.environ.get("EMAIL")
app_password = os.environ.get("PASSWORD")
recipients = RECIPIENT1

gemini_response = completion

msg = EmailMessage()
msg["Subject"] = "پیش‌بینی هوا با مامان پوری🌤️"
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


