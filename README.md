# Write an HTTP service in Python

## Support the following transactions:

* POST - write request body (a ‘block’ - anywhere from 1 byte to 64 MiB) content to disk. Respond with sha1 hash of data.

* GET - given a sha1, respond with data previously POSTed

Cases to consider / test:
* Write a block
* Read a block (verify sha1)
* Concurrent writes
* Concurrent write with same data content
* Disk full
* Nonexistent data requested
* Write a block that already exists on disk
* Data corrupt on disk

### Installing

We are using python & flask with virtual env. So first create virtual env:
```
virtualenv env
source env/bin/activate
```

To Install all dependencies
```
pip install -r requirements.txt
```

### Start App

```
FLASK_APP=server.py flask run
```


### Test POST (python code)

```
import requests

url = "http://127.0.0.1:5000/post-data"

payload = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
headers = {'cache-control': "no-cache"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
```

### Test GET (python code)
```
import requests

url = "http://127.0.0.1:5000/get-data/e7505beb754bed863e3885f73e3bb6866bdd7f8c"
headers = {'cache-control': "no-cache"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```