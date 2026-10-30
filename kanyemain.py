import json
import smtplib
import requests
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
RECIPIENT1 = os.environ.get("RECIPIENT1")
RECIPIENT2 = os.environ.get("RECIPIENT2")

with requests.get("https://api.kanye.rest/") as response:
    data = response.json()
    quote = data.get('quote')
    with open("kanye.json", "r") as file:
        try:
            data = json.load(file)
            data.update({"quote": f"updated as {quote}"})
        except:
            with open("kanye.json", "w") as file:
                json.dump(data, file)
        else:
            with open("kanye.json", "w") as file:
                json.dump(data, file)
print(quote)
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(from_addr=EMAIL, to_addrs=[RECIPIENT1, RECIPIENT2],
                        msg=f"Subject: And so said Kanye...\n\n {quote}")
