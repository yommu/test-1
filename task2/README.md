# Write an HTTP storage client in Python

## REquirements:

* Given a block of data (up to 64 MiB) and an ordered list of servers, send the data to the first two servers using two asynchronous POST requests. If one fails, let the other continue while initiating a third request on the third server. Continue until two different servers have reported success.

* To test your client, write a stub server that accepts data, discards the data, and reports HTTP 200, say, 30% of the time, and only after a variable delay.


### Installing

` These steps needs to be done in root folder of repo.`

We are using python & flask with virtual env. So first create virtual env:
```
virtualenv env
source env/bin/activate
```

To Install all dependencies
```
pip install -r requirements.txt
```

### Starting servers

```
FLASK_APP=server.py FLASK_DEBUG=1 python -m flask run --port=8881
FLASK_APP=server.py FLASK_DEBUG=1 python -m flask run --port=8882
FLASK_APP=server.py FLASK_DEBUG=1 python -m flask run --port=8883
```

After this you will be able to make post requests to urls:
```
http://127.0.0.1:8881
http://127.0.0.1:8882
http://127.0.0.1:8883
```


### Client

```
python client.py
```