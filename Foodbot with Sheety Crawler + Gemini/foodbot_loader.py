import os
import requests
import json
# from dotenv import load_dotenv
# load_dotenv()

TOKEN = os.environ.get("TOKEN")
bearer_headers = {
"Authorization": f"Bearer {os.environ.get("TOKEN")}",
}

sheety_endpoint = "https://api.sheety.co/938b7f92e00f05078c980ef49b560c3f/100DaysOfPython"
class FoodBot:
    def __init__(self, sheet_name="foodForm"):
        self._api_key = TOKEN
        self._sheety_endpoint = f"{sheety_endpoint}/{sheet_name}"
        self._headers = bearer_headers
        self.sheet_data = {}

    def get_sheet_data(self):
        response = requests.get(self._sheety_endpoint, headers=self._headers)
        self.sheet_data = response.json()
        print(self.sheet_data)
        return self.sheet_data


