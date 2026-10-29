import json
import requests
from datetime import datetime
import smtplib
import time
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
MY_LAT = os.environ.get("MY_LAT")
MY_LON =  os.environ.get("MY_LON")

def is_iss_above():
    with requests.get("http://api.open-notify.org/iss-now.json") as iss_response:
        iss_response.raise_for_status()
        iss_data = iss_response.json()
        iss_lat = float(iss_data.get("iss_position").get("latitude"))
        iss_lon = float(iss_data.get("iss_position").get("longitude"))
        with open("iss-now.json", "w") as file:
            json.dump(iss_data, file, indent=4)
        print(iss_lat)
        print(iss_lon)
    # return iss_lat, iss_lon
    if float(MY_LAT)-5 <= iss_lat <= float(MY_LAT)+5 and float(MY_LON)-5 <= iss_lon <= float(MY_LON)+5:
        return True


def is_it_dark():
    params = {
        "lat" : MY_LAT,
        "lng" : MY_LON,
        "formatted" : 0,
    }
    with requests.get("https://api.sunrise-sunset.org/json", params = params) as sun_response:
        sun_response.raise_for_status()
        sun_data = sun_response.json()
        with open("sunriseset.json", "w") as file:
            json.dump(sun_data, file, indent=4)
    sunrise = int(sun_data.get("results").get("sunrise").split("T")[1].split(":")[0])
    sunset = int(sun_data.get("results").get("sunset").split("T")[1].split(":")[0])
    print(sunrise)
    print(sunset)
    now = datetime.now()
    my_hour = int(now.hour)
    if my_hour >= sunset or my_hour <= sunrise:
        return True

def send_email():
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=["milad.foroughan@gmail.com", "naz.rahnama@gmail.com"],
                            msg=f"Subject: Look UP!\n\n ISS Is Now Passing Right Above Your Head...")

is_it_dark()
is_iss_above()
while True:
    time.sleep(300)
    if is_it_dark() and is_iss_above():
        send_email()



# ----------------------------------------------////-------------------------------------- #
