import threading
import time
import requests

data_payload = "This is test data"
servers = ['http://127.0.0.1:8881', 'http://127.0.0.1:8882', 'http://127.0.0.1:8883']

class DataSender:

    def __init__(self, servers, data):
        self.servers = servers
        self.data = data

    def start(self):
        self.use_one_server()
        self.use_one_server()

    def use_one_server(self):
        t = threading.Thread(target=self.send)
        t.start()

    def send(self):
        server = self.servers.pop(0)

        print "%s :Starting" % server

        try:
            r = requests.post(server, self.data)
            if r.status_code == 200:
                self.success(server)
            else:
                self.fail(server)
        except (requests.ConnectionError) as e:
            self.fail(server)

    def success(self, server):
        print "%s :Success" %server

    def fail(self, server):
        print "%s :Fail" % server
        self.servers.append(server)
        self.use_one_server()

datasender = DataSender(servers, data_payload)
datasender.start()
print datasender.servers
