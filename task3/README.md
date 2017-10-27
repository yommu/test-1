# Write an in-memory query engine in Python

## Transactions:

* POST - Store an object. An object consists of an identifier (an arbitrary string) and a list of numeric ranges. 
<br />Example:<br />
```{”identifier”: ”foo”, ”ranges”: [[12,34],[37,440],[460,800]]}```
<br />If an object already exists with the same identifier, overwrite it & return success.
* GET - Retrieve a list of objects whose ranges overlap a specified range. <br />Example:<br />
Request: ```[440,464]```
Response: ```[{”identifier”: ”foo”,”ranges”:[[37,440],[460,800]],”intersection”:6}]```
<br />(because [440,464] overlaps [37,440] by 1 position and [460,800] by 5 positions)

### Starting servers

```
FLASK_APP=server.py FLASK_DEBUG=1 python -m flask run --port=8881
```

### Test POST (python code)

```
import requests

url = "http://127.0.0.1:8881/"

payload = "{\"identifier\": \"foo\",\n \"ranges\": [[0, 34000],[37,440],[460,800]]\n}"
headers = {'cache-control': "no-cache"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
```

### Test GET (python code)
```
import requests

url = "http://127.0.0.1:8881/[440, 464]"
headers = {'cache-control': "no-cache"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```