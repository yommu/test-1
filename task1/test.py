import requests

url = "http://127.0.0.1:5000/post-data"

payload = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
headers = {'cache-control': "no-cache"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

url = "http://127.0.0.1:5000/get-data/e7505beb754bed863e3885f73e3bb6866bdd7f8c"
headers = {'cache-control': "no-cache"}

response = requests.request("GET", url, headers=headers)

print(response.text)