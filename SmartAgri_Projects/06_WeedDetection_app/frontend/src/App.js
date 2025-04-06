import React, { useState } from 'react';
import { Container, Typography } from '@mui/material';
import VideoUpload from './components/VideoUpload';
import VideoDisplay from './components/VideoDisplay';
import './App.css';
function App() {
  const [uploadSuccessful, setUploadSuccessful] = useState(false);
  const [resetUpload, setResetUpload] = useState(false);  // New state

  const handleUploadSuccess = () => {
    setUploadSuccessful(true);
    setResetUpload(false);  // Ensure reset is false on successful upload
  };

  const handleNewUpload = () => {
    setUploadSuccessful(false);  // Reset on new upload initiation
    setResetUpload(true);  // Indicate a reset is happening
  };

  return (
    <div className="App">
      <img src="/logo.jpeg" alt="logo" className='header-image' />
      <h2 className='header-text'>Precision Agriculture</h2>
      <Container maxWidth="md">
      <Typography variant="h5" align="center" paragraph>
      Upload a video to track weeds in your field.
      </Typography>
      <VideoUpload onUploadSuccess={handleUploadSuccess} onNewUpload={handleNewUpload} />
      {uploadSuccessful && <VideoDisplay uploadSuccessful={uploadSuccessful} resetUpload={resetUpload} />}
      
    </Container>
    </div>
  );
}

export default App;