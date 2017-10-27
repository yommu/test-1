from flask import Flask, abort, request, make_response, json
import random
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recive():

    # Sleep randomply from 5 to 20 sec
    time.sleep(random.randint(1, 3))

    if random.randint(0, 100) < 30:
        return make_response('Success')
    else:
        return json.jsonify(error=500, text="Error"), 500
