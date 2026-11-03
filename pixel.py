import datetime as dt
import requests

graph_config_params = {
    "id": "mygraph1",
    "name": "MyPythonGraph",
    "unit": "hr",
    "type": "float",
    "color": "sora",
}

TOKEN = "ntqc3typdxm43xp,qz"
USERNAME = "milad8600"
endpoint = "https://pixe.la/v1/users"
graph_endpoint = f"{endpoint}/{USERNAME}/graphs/{graph_config_params['id']}"
pixel_endpoint = f"{endpoint}/{USERNAME}/graphs/{graph_config_params['id']}"

headers = {
    "X-USER-TOKEN":TOKEN,
}

profile_creation_params = {
    "token":TOKEN,
    "username":USERNAME,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}

# response = requests.post(url=endpoint, json=profile_creation_params)
# print(response.text)



# response = requests.put(url=graph_endpoint, headers=headers, json=graph_config_params)
# print(response.text)

now = dt.datetime.now()
today = now.strftime("%Y%m%d")
print(today)

# with open("sample.json", "r") as file:
#     data = json.load(file)
# print(data)

QUANTITY = input("How long did you spend today on Python?")
pixel_config_params = {
    "date": today,
    "quantity": QUANTITY,
    # "optionalData": str(data),
}

try:
    response = requests.post(url=pixel_endpoint, json=pixel_config_params, headers=headers)
    print(response.text)
except Exception as e:
    print(e)
