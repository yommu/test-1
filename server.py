from flask import Flask, abort, request, make_response, json
import hashlib
import sys
import time, os, stat

app = Flask(__name__)

data_path = "data"

if os.path.isdir(data_path) is not True:
    os.mkdir(data_path)

class LockWaiter:

    def __init__(self, number_of_tryes):
        self.number_of_tryes = number_of_tryes
        self.wait_time = 1

    def get_file_lock_name(self, file_path):
        return file_path + ".lock"

    def lock(self, file_path):
        lock_file_path = self.get_file_lock_name(file_path)
        open(lock_file_path, 'a').close()

    def unlock(self, file_path):
        lock_file_path = self.get_file_lock_name(file_path)
        os.remove(lock_file_path)

    def file_available(self, file_path):
        if self.number_of_tryes == 0:
            return False
        else:
            lock_file_path = file_path + ".lock"

            if os.path.isfile(lock_file_path):

                lock_removed = self.delete_file_if_older(lock_file_path, 60)
                if lock_removed is True:
                    return self.file_available(file_path)

                self.number_of_tryes -= 1
                time.sleep(self.wait_time)
                return self.file_available(file_path)
            else:
                return True

    def delete_file_if_older(self, file_path, max_age_seconds):
        age_seconds = self.file_age_in_seconds(file_path)

        if age_seconds > max_age_seconds:
            os.remove(file_path)
            return True
        else:
            return False

    def file_age_in_seconds(self, pathname):
        return time.time() - os.stat(pathname)[stat.ST_MTIME]

@app.route('/post-data', methods=['POST'])
def recive():
    data     = request.data
    datasize = len(data.encode("utf8"))

    if datasize < 1 or datasize > 64*1024*1024:
        return json.jsonify(error=400, text='Data needs to be more that 1B and less that 64MiB size'), 400

    hash_string    = hashlib.sha1(data).hexdigest()
    file_path      = os.path.join(data_path, hash_string)
    lock_file_path = file_path + ".lock"
    locker   = LockWaiter(2)

    if locker.file_available(file_path) is not True:
        return json.jsonify(error=400, text='File is locked, try again later'), 400

    locker.lock(file_path)

    if os.path.isfile(file_path) is not True:
        with open(file_path, "w", 0) as new_file:
            new_file.write(data)

    locker.unlock(file_path)

    return make_response(hash_string)

@app.route('/get-data/<sha1>', methods=['GET'])
def send(sha1):
    file_path = os.path.join(data_path, sha1)

    if os.path.isfile(file_path):
        with open(file_path, "r") as hash_file:
            return make_response(hash_file.read())

    return json.jsonify(error=404, text='File does not exists'), 404
