"""Unit tests for the emotion detector."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Test emotion detection results and HTTP error handling."""

    def setUp(self):
        self.emotions = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.90,
            "sadness": 0.04,
        }

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_successful_detection(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": self.emotions}]
        }
        mock_post.return_value = response

        result = emotion_detector("I am happy")

        self.assertEqual(result["joy"], 0.90)
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(len(result), 6)
        response.raise_for_status.assert_called_once()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none(self, mock_post):
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response

        self.assertIsNone(emotion_detector("invalid input"))
        response.raise_for_status.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input_returns_none(self, mock_post):
        self.assertIsNone(emotion_detector("   "))
        mock_post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_emotion_is_highest_score(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.70,
                    "disgust": 0.10,
                    "fear": 0.05,
                    "joy": 0.10,
                    "sadness": 0.05,
                }
            }]
        }
        mock_post.return_value = response

        result = emotion_detector("I am furious")
        self.assertEqual(result["dominant_emotion"], "anger")


if __name__ == "__main__":
    unittest.main()
