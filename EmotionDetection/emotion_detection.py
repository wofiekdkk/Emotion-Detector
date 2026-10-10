"""Emotion detection using the IBM Watson NLP service."""

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion, or None on HTTP 400."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(
        API_URL, json=payload, headers=headers, timeout=10
    )

    if response.status_code == 400:
        return None

    response.raise_for_status()
    data = response.json()
    emotions = data["emotionPredictions"][0]["emotion"]

    scores = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }
    scores["dominant_emotion"] = max(scores, key=scores.get)
    return scores
