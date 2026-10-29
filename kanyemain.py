import json
import smtplib
import requests
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

with requests.get("https://api.kanye.rest/") as response:
    data = response.json()
    quote = data.get('quote')
    # with open("kayne.json", "r") as file:
    #     try:
    #         data = json.load(file)
    #         data.update({"quote": f"updated as {quote}"})
    #     except:
    #         with open("kayne.json", "w") as file:
    #             json.dump(data, file)
    #     else:
    #         with open("kayne.json", "w") as file:
    #             json.dump(data, file)
# print(quote)
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(from_addr=email, to_addrs=["milad.foroughan@gmail.com"],
                        msg=f"Subject: And so said Kanye...\n\n {quote}")
