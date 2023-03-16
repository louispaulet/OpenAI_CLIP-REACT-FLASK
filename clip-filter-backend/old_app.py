#this is the previous iteration of app.py -- keep it for future ideas

import base64
import json
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from PIL import Image
import io
from transformers import CLIPProcessor, CLIPModel

app = Flask(__name__)
CORS(app)

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

@app.route("/clip_filter", methods=["POST"])
def image_similarity():
	try:
		if not request.is_json:
			return json.dumps({"error": "Invalid request"}), 400
		if "image_data" not in request.json:
			return jsonify({"error": "image_data key is missing in the request payload"}), 400

		image_data_list = request.json["image_data"]
		text = request.json["text"]

		if not image_data_list or not text:
			return json.dumps({"error": "Invalid data"}), 400

		base64_images = request.json["image_data"]
		text = request.json["text"]

		if not base64_images or not text:
			return json.dumps({"error": "Invalid data"}), 400

		similarities = []

		for base64_image in base64_images:
			imgdata = base64.b64decode(base64_image)
			image = Image.open(io.BytesIO(imgdata))
			
			if image.mode == "RGBA":
				image = image.convert("RGB")  # Remove the alpha channel

			#print("Image mode:", image.mode)  # Debug print
			#current_app.logger.info("Image mode: %s", image.mode)  # Debug print using Flask logger
			#current_app.logger.info("Logits per text shape: %s", str(logits_per_text.shape))

			image = image.resize((224, 224))  # Resize the image to 224x224

			inputs = processor(text=text, images=image, return_tensors="pt", padding=True)

			pixel_values = inputs['pixel_values']
			input_ids = inputs['input_ids']

			current_app.logger.info("Pixel values shape: %s", str(pixel_values.shape))  # Debug print using Flask logger
			current_app.logger.info("Input ids shape: %s", str(input_ids.shape))  # Debug print using Flask logger

			logits_per_image, logits_per_text = model(pixel_values, input_ids)
			probs = logits_per_image.softmax(dim=-1).tolist()

			current_app.logger.info("Logits per image shape: %s", str(logits_per_image.shape))  # Debug print using Flask logger
			current_app.logger.info("Logits per text shape: %s", str(logits_per_text.shape))  # Debug print using Flask logger
			current_app.logger.info("Probs: %s", str(probs))  # Debug print using Flask logger

			similarities.append(probs[0][0])

		response = {
			"similarities": similarities
		}

		return json.dumps(response), 200

	except Exception as e:
		print(str(e))  # Print the error message to the console
		return json.dumps({"error": "An error occurred: " + str(e)}), 500

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
