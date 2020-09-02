import markdown
from flask import Flask, render_template, request, jsonify, make_response
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import random
import json
import requests
import re


app = Flask(__name__)
app.static_folder = "static"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/urban", methods=["GET", "POST"])
def webhook():
    # parse data from request
    if request.method == "POST":
        req = request.get_json(silent=True, force=True)
        params = req["queryResult"]["parameters"]
        if "phrase" in params and params["phrase"] is not None:
            phrase = params["phrase"]
            print(phrase)
            res = define(phrase)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"]="application/json"
    return r

def define(phrase):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    querystring = {"term": phrase}

    headers = {
        "x-rapidapi-host": "mashape-community-urban-dictionary.p.rapidapi.com",
        "x-rapidapi-key": "a9520b2012mshe2a098d392901cfp18b21ejsn7cd5055df26e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    definition = json.loads(response.text)

    # parse definition from json
    if "definition" in definition["list"][0]:
        definition = definition["list"][0]["definition"]
        definition = definition.replace("[", "")
        definition = definition.replace("]", "")
        print(definition)
        return fulfillment_message(definition)
    else:
        return fulfillment_message("no definition was found")

def fulfillment_message(text):
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        text
                    ]
                }
            }
        ]
    }


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port=5000)
