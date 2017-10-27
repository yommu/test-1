from flask import Flask, abort, request, make_response, json, jsonify
import random
import time
import jsonschema

app = Flask(__name__)

memory_data = dict()

post_data_schema = {
  "type": "object",
  "required": [
    "identifier",
    "ranges"
  ],
  "properties": {
    "identifier": {
      "type": "string"
    },
    "ranges": {
      "type": "array",
      "items": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "minItems": 2,
        "maxItems": 2
      }
    }
  }
}

get_data_schema = {
    "type": "array",
    "items": {
        "type": "number"
    },
    "minItems": 2,
    "maxItems": 2
}

@app.route('/', methods=['POST'])
@app.route('/<range_arg>', methods=['GET'])
def api(range_arg = None):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            jsonschema.validate(data, post_data_schema)
            store_data(data)
            return make_response("Success")
        except (ValueError, jsonschema.ValidationError) as e:
            return json.jsonify(error=400, text=str(e)), 400
    else:
        if range_arg is None:
            return make_response('[]')

        try:
            data = json.loads(range_arg)
            jsonschema.validate(data, get_data_schema)
        except (ValueError, jsonschema.ValidationError) as e:
            return json.jsonify(error=400, text=str(e)), 400

        result = [get_intersactions_data(data, identifier) for identifier in memory_data]

        return jsonify(result)

def store_data(data):
    if 'identifier' not in data:
        raise ValueError('could not find identifier in %s' % str(data))

    if 'ranges' not in data:
        raise ValueError('could not find ranges in %s' % str(data))

    memory_data[data["identifier"]] = data["ranges"]

def get_intersactions_data(data, identifier):
    item = {
        "identifier": identifier,
        "ranges": [],
        "intersection": 0
    }

    for _range in memory_data[identifier]:
        intersection_length = get_intersection_length(data, _range)
        if intersection_length > 0:
            item["ranges"].append(_range)
            item["intersection"] += intersection_length

    return item

def get_intersection_length(first, second):
    return len(range(max(first[0], second[0]), min(first[-1], second[-1])+1))
