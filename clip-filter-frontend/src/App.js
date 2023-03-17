import React, { useState } from 'react';
import './App.css';

function App() {
  const [images, setImages] = useState([]);
  const [textInput1, setTextInput1] = useState('');
  const [textInput2, setTextInput2] = useState('');
  const [results, setResults] = useState([]);

  async function submitForm() {
	  for (const imageFile of images) {
		const reader = new FileReader();
		reader.onloadend = async () => {
		  const imageBase64 = reader.result.split(',')[1];
		  const response = await fetch('http://localhost:5000/image_text_similarity_best_match', {
			method: 'POST',
			headers: {
			  'Content-Type': 'application/json',
			},
			body: JSON.stringify({
			  image_base64: imageBase64,
			  text_input1: textInput1,
			  text_input2: textInput2,
			}),
		  });

		  const data = await response.json();
		  setResults((prevResults) => [
			...prevResults,
			{
			  thumbnail: URL.createObjectURL(imageFile),
			  text: 'Best matching text for ' + imageFile.name + ': ' + data.best_match,
			},
		  ]);
		};
		reader.readAsDataURL(imageFile);
	  }
	}


  function handleFileSelect(event) {
    event.preventDefault();
    event.stopPropagation();

    const files = event.dataTransfer.files;
    updateImagePreviews(files);
  }

  function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    event.dataTransfer.dropEffect = 'copy';
  }

  function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
  }

  function updateImagePreviews(files) {
    const fileList = Array.from(files);
    setImages(fileList);
  }
  
  return (
  <div className="container">
    <h1>Image Text Similarity</h1>
    <form onSubmit={(event) => { event.preventDefault(); submitForm(); }}>
      <div
        id="drop-zone"
        className="drop-zone"
        onDrop={handleFileSelect}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        Drop images here or click to select
        <input
          type="file"
          id="image-input"
          accept="image/*"
          multiple
          style={{ display: 'none' }}
          onChange={(e) => updateImagePreviews(e.target.files)}
        />
      </div>
      <br />
      <div id="preview-container">
        {images.map((imageFile, index) => (
          <img
            key={index}
            src={URL.createObjectURL(imageFile)}
            alt="Selected Image Preview"
            style={{ maxWidth: '100%', maxHeight: '300px' }}
          />
        ))}
      </div>
      <br />
      <label htmlFor="text-input1">Text Input 1:</label>
      <input
        type="text"
        id="text-input1"
        value={textInput1}
        onChange={(e) => setTextInput1(e.target.value)}
        required
      />
      <br />
      <label htmlFor="text-input2">Text Input 2:</label>
      <input
        type="text"
        id="text-input2"
        value={textInput2}
        onChange={(e) => setTextInput2(e.target.value)}
        required
      />
      <br />
      <button type="submit">Find Best Match</button>
    </form>
    <ul id="result">
	  {results.map((result, index) => (
		<li key={index}>
		  <img
			src={result.thumbnail}
			alt="Thumbnail"
			style={{ maxWidth: '50px', maxHeight: '50px', marginRight: '10px' }}
		  />
		  {result.text}
		</li>
	  ))}
	</ul>
  </div>
);

}

export default App;