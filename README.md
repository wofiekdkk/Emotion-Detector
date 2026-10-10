# Emotion Detector

A Python Flask application that uses IBM Watson NLP to identify five
emotions in text: anger, disgust, fear, joy, and sadness.

## Requirements

Python 3.9 or compatible, plus network access to the course NLP endpoint.

## Install

    python -m pip install -r requirements.txt

## Run unit tests

    python -m unittest -v test_emotion_detection

## Run the web application

    python server.py

Open http://127.0.0.1:5000 in your browser.

## Static analysis

    python -m pylint server.py
