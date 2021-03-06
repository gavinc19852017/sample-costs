#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "Bus-ticket-price":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("Departure-location")

    cost = {'Home':5, 'City':7, 'Roma Street':4.50, 'Wooloongabba':7.65, 'ann street':8.50, 'Blunder road':7.25, 'Moggill road':8.75}

    speech = "The price for your journey to " + zone + " is " + str(cost[zone]) + " dollars."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "Gavins-greatest"
        #Random text
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
