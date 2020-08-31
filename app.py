import markdown
from flask import Flask, render_template, request, jsonify, make_response
from flask_assistant import Assistant, ask
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import random
import json

app = Flask(__name__)
app.static_folder = "static"

# initialize Assistant
assistant = Assistant(app, '/google')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mdtest")
def markdown_render():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
                         readme_file.read(), extensions=["fenced_code"])

    formatter = HtmlFormatter(style="emacs", full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"

    return md_css_string + md_template_string



@app.route("/random", methods=["GET", "POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = get_random_number()
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type']='application/json'
    return r

def get_random_number():
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        str(random.randint(0,100))
                    ]
                }
            }
        ]
    }


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.run(ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
    app.run(port=5000)
