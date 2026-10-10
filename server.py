"""Flask web application for emotion detection."""

import requests
from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Display the emotion detector interface."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["POST"])
def detect_emotion():
    """Process the submitted text and display its detected emotions."""
    text_to_analyze = request.form.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return (
            render_template(
                "index.html",
                error="Please enter some text to analyze.",
                input_text=text_to_analyze,
            ),
            400,
        )

    try:
        result = emotion_detector(text_to_analyze)
    except (requests.exceptions.RequestException, ValueError):
        return (
            render_template(
                "index.html",
                error="The emotion service could not process your request.",
                input_text=text_to_analyze,
            ),
            502,
        )

    if result is None:
        return (
            render_template(
                "index.html",
                error="The service rejected the input.",
                input_text=text_to_analyze,
            ),
            400,
        )

    return render_template(
        "index.html",
        input_text=text_to_analyze,
        result=result,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
