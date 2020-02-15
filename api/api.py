import flask
from flask import request, jsonify, render_template

from api.modules.Cleaner import Cleaner
from api.modules.Fetcher import Fetcher
from api.modules.Segmenter import Segmenter
from api.modules.Classifier import Classifier
from api.modules.ResponseProcessor import ResponseProcessor
from api.models.ApiException import ApiException
from api.models.KeyDescription import descriptions

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pytz
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/analyse', methods=['POST'])
def analyser():
    url = request.form.get('url')
    if url is not None:
        source = Fetcher.fetch(url, driver)
        tags = Cleaner.clean(source)
        annotations = Segmenter.segment(tags)

        annotations, analysis = Classifier.run(annotations)

        if analysis.count() < 15:
            raise ApiException("Invalid Policy Document", "The page is not a valid policy document", 400)

        response = ResponseProcessor.run(annotations, analysis)

        return jsonify(response)
    else:
        raise ApiException("Invalid Input", "No request arguments entered", 400)


@app.route('/api/annotate', methods=['POST'])
def annotate():
    url = request.form.get('url')
    if url is not None:
        source = Fetcher.fetch(url, driver)
        tags = Cleaner.clean(source)
        annotations = Segmenter.segment(tags)

        annotations, _ = Classifier.run(annotations)

        response = []
        for annotation in annotations:
            response.append({
                "attributes": annotation.attributes,
                "categories": annotation.categories,
                "text": annotation.text
            })

        return jsonify(response)
    else:
        raise ApiException("Invalid Input", "No request arguments entered", 400)


@app.route('/api/help', methods=["GET"])
def help_handler():
    key = request.args.get("key")
    description = descriptions.get(key.replace("-", " "))
    response = {
        "value": key,
        "description": description
    }
    return jsonify(response)


@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(500)
def handle_404_exception(error):
    london = pytz.timezone("Europe/London")
    response = jsonify({
        "timestamp": datetime.now(london).strftime("%d-%m-%YT%H:%M:%S"),
        "status": error.code,
        "error": error.name,
        "message": error.description
    })
    response.status_code = error.code
    return response


@app.errorhandler(ApiException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.run()
