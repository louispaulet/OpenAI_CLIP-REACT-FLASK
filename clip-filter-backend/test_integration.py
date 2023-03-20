import unittest
import requests
import base64

class TestImageTextSimilarityIntegration(unittest.TestCase):
    def test_api_image_text_similarity_best_match(self):
        # Load and encode a sample image to base64
        with open("sample_image.jpg", "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        # Define the request payload
        data = {
            "image_base64": image_base64,
            "text_input1": "text 1",
            "text_input2": "text 2"
        }

        # Send a POST request to the API
        response = requests.post("http://localhost:5000/image_text_similarity_best_match", json=data)

        # Check if the response is successful and the result is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()["best_match"], ["text 1", "text 2"])

if __name__ == "__main__":
    unittest.main()
