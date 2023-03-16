import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [images, setImages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [filteredImages, setFilteredImages] = useState([]);
  const [notFilteredImages, setNotFilteredImages] = useState([]);

  const onImageDrop = (e) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    Promise.all(files.map(file => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
          resolve({ file, src: event.target.result });
        };
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
      });
    }))
    .then(images => {
      setImages(images);
    });
  };

  const onDragOver = (e) => {
    e.preventDefault();
  };

  const onInputChange = (e) => {
    setInputText(e.target.value);
  };

const onFilterClick = async () => {
    try {
      const base64Images = images.map((image) => {
        return image.src.split(',')[1];
      });
      const response = await axios.post('http://localhost:5000/clip_filter', {
        image_data: base64Images,
        text: inputText,
      });
      
      const similarities = response.data.similarities;
      const similarityThreshold = 0.5; // Adjust this value to change the filtering criteria

      const filtered = [];
      const notFiltered = [];

      images.forEach((image, index) => {
        if (similarities[index] >= similarityThreshold) {
          filtered.push(image);
        } else {
          notFiltered.push(image);
        }
      });

      setFilteredImages(filtered);
      setNotFilteredImages(notFiltered);
      
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <div className="drop-area" onDrop={onImageDrop} onDragOver={onDragOver}>
        <p>Drag & Drop Images Here</p>
        <div className="preview">
          {images.map((image, index) => (
            <img key={index} src={image.src} alt={`Uploaded-${index}`} />
          ))}
        </div>
      </div>
      <div className="filter">
        <input
          type="text"
          placeholder="Filter description"
          value={inputText}
          onChange={onInputChange}
        />
        <button onClick={onFilterClick}>Filter Images</button>
      </div>
      <div className="results">
        <div className="filtered-images">
          <h3>Filtered Images</h3>
          {filteredImages.map((image, index) => (
            <img key={index} src={image.src} alt={`Filtered-${index}`} />
          ))}
        </div>
        <div className="not-filtered-images">
          <h3>Not Filtered Images</h3>
          {notFilteredImages.map((image, index) => (
            <img key={index} src={image.src} alt={`NotFiltered-${index}`} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
