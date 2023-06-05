## dependencies, run: pip install -r requirements.txt in terminal first to ensure environment consistency
import requests

## construct request
url = "https://api.ipcinfo.org/areas"
api_key = "3a808893-e3d5-4067-a57a-c5b3a9bec662" ## replace with your own api key (delete this line after publication)
params = {
    "format": "geojson",
    "type": "A",
    "key": api_key
}
headers = {
    "accept": "application/geo+json"
}

## send request
response = requests.get(url, params=params, headers=headers)
encoded_text = response.text.encode("utf-8")
if response.status_code == 200:
    print("Success!")
    with open("output.geojson", "wb") as f:
        f.write(encoded_text)
else:
    print("Request failed with status code:", response.status_code)

