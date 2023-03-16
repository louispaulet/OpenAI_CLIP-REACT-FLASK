from flask import Flask, request, jsonify
from PIL import Image
import io
from io import BytesIO
import base64
import json
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from PIL import Image
import torch
from sklearn.metrics.pairwise import cosine_similarity


from transformers import CLIPProcessor, CLIPModel

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": ["*", "null"]}})

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

@app.route('/image_text_similarity_best_match', methods=['POST'])
def api_image_text_similarity_best_match():
	data = request.json
	image_data = base64.b64decode(data['image_base64'])
	text_input1 = data['text_input1']
	text_input2 = data['text_input2']

	image = Image.open(BytesIO(image_data))

	best_match = image_text_similarity_best_match(image, text_input1, text_input2)
	return jsonify({"best_match": best_match})

def image_text_similarity_best_match(image: Image.Image, text_input1: str, text_input2: str) -> str:
	# Process the image and both text inputs
	image_input = processor(images=image, return_tensors="pt", padding=True)
	text_input1_processed = processor(text=text_input1, return_tensors="pt", padding=True)
	text_input2_processed = processor(text=text_input2, return_tensors="pt", padding=True)

	# Get the embeddings
	with torch.no_grad():
		image_embedding = model.get_image_features(**image_input)
		text_embedding1 = model.get_text_features(**text_input1_processed)
		text_embedding2 = model.get_text_features(**text_input2_processed)

	# Calculate the cosine similarities
	cosine_sim1 = cosine_similarity(image_embedding, text_embedding1)
	cosine_sim2 = cosine_similarity(image_embedding, text_embedding2)

	# Return the text input with the highest cosine similarity
	if cosine_sim1 > cosine_sim2:
		return text_input1
	else:
		return text_input2

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
