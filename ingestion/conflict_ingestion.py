import requests

url = "https://acleddata.com/acleddatanew.csv"

response = requests.get(url)

with open("data/raw/conflict/acled.csv", "wb") as f:
    f.write(response.content)

print("Conflict dataset downloaded")