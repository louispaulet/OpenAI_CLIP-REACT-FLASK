import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
from app import image_text_similarity_best_match

class TestImageTextSimilarityUnit(unittest.TestCase):
    @patch("app.processor")
    @patch("app.model")
    def test_image_text_similarity_best_match(self, mock_model, mock_processor):
        # Mock the processor and model functions
        mock_model.get_image_features.return_value = [[0.5, 0.6]]
        mock_model.get_text_features.side_effect = [[[0.7, 0.8]], [[0.6, 0.5]]]
        mock_processor.return_value = None

        # Load a sample image
        with open("sample_image.jpg", "rb") as image_file:
            image = Image.open(image_file)

        # Call the function and check the result
        result = image_text_similarity_best_match(image, "text 1", "text 2")
        self.assertEqual(result, "text 1")

if __name__ == "__main__":
    unittest.main()
