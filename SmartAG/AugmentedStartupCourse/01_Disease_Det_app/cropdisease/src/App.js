import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [processedImage, setProcessedImage] = useState(null);
  const [detectedLabel, setDetectedLabel] = useState(null);  // State for label
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [warning, setWarning] = useState("");
  const [isChatLoading, setChatLoading] = useState(false);
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    setMessages([]);  // Clear chat history
    setProcessedImage(null);
    setDetectedLabel(null);
    setLoading(false);
    setWarning("");
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setImage(reader.result);
    };
  };
  const handleSendMessage = () => {
    if (userInput.trim() === '') {
      setWarning("Please enter a message.");
      setTimeout(() => {
          setWarning("");
      }, 2000);
      return;
    }
    setChatLoading(true);
    
    const payload = {
      message: userInput,
      chatHistory: messages // This sends the chat history
    };
    fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify( payload ),
    })
      .then(response => response.json())
      .then(data => {
        setMessages([...messages, { sender: 'user', text: userInput }, { sender: 'bot', text: data.response }]);
        setChatLoading(false);
      })
      .catch(error => console.error('Error:', error));
  
    setUserInput(''); // Reset input after sending
    setWarning(""); // Clear the warning
  };
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };


  const handleProcessImage = () => {
    setLoading(true);

    const blob = dataURLtoBlob(image);
    const formData = new FormData();
    formData.append('file', blob);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        const imgURL = `data:image/jpeg;base64,${data.image}`;
        setProcessedImage(imgURL);
        setDetectedLabel(data.label);
        setLoading(false);
        setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: `Detected Diseases: ${data.label}` }, { sender: 'bot', text: "How can we assist you?" }]);
      })
      .catch((error) => {
        console.error('Error:', error);
        setLoading(false);
      });
  };

  const dataURLtoBlob = (dataurl) => {
    const arr = dataurl.split(',');
    const mimeMatch = arr[0].match(/:(.*?);/);

    if (!mimeMatch) {
      throw new Error('Invalid MIME type');
    }

    const mime = mimeMatch[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new Blob([u8arr], { type: mime });
  };

return (
  
  <div className="container mt-5">
    <h1 className="text-center">Crop Disease Identification</h1>
    
    
    
    <div className="app-body d-flex">
      
      <div className="left-content">
      <img src="/download.png" alt="Header" className="header-image" />
        {image && (
          <div className="mt-4">
            <h3>Preview</h3>
            <img src={image} alt="Preview" className="img-thumbnail" />
          </div>
        )}
        <div className="mt-4">
          <input type="file" accept="image/*" className="form-control-file" onChange={handleImageChange} />
          <button className="btn btn-primary mt-3" onClick={handleProcessImage}>Process</button>
        </div>
        {loading && (
          <div className="mt-4">
            <div className="spinner-border text-primary" role="status">
              <span className="sr-only">Loading...</span>
            </div>
            <p>Image is being processed...</p>
          </div>
        )}

        {processedImage && (
          <div className="mt-4">
            <h3>Processed Image</h3>
            <img src={processedImage} alt="Processed" className="img-thumbnail" />

            {detectedLabel && (
              <div className="mt-2">
                <strong>Detected Diseases:</strong> {detectedLabel}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="right-content">
        <div className="chatbox">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <p>{message.text}</p>
            </div>
          ))}
          {isChatLoading && (
            <div className="message loading">
            <div className="spinner-border text-primary" role="status">
                <span className="sr-only">Loading...</span>
            </div>
            </div>
          )}
        </div>
        {warning && <p className="warning-message">{warning}</p>}
        <div className="input-area">
        
          <input type="text" value={userInput} 
          onChange={(e) => setUserInput(e.target.value)} 
          onKeyPress={handleKeyPress} 
          placeholder="Type a message..." 
          disabled={!processedImage || isChatLoading}/>
          <button onClick={handleSendMessage}
          disabled={!processedImage || isChatLoading}>
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
);
}

export default App;