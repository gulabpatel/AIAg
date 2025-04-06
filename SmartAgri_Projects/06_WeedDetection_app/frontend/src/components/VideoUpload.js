import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Button, Box, LinearProgress, Stack } from '@mui/material';
import { PlayArrow as PlayArrowIcon, CloudUpload as CloudUploadIcon } from '@mui/icons-material';

const VideoUpload = ({ onUploadSuccess, onNewUpload }) => {
  const [video, setVideo] = useState(null);
  const [uploadPercentage, setUploadPercentage] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const fileInput = useRef(null);

  const handleVideoChange = (event) => {
    const file = event.target.files[0];
    if (!file) {
      console.error('No file selected');
      return;
    }

    setVideo(file);
    onNewUpload();  // Assuming this is for resetting any video state in the parent component
  };

  const uploadVideo = async () => {
    if (!video) return;

    const formData = new FormData();
    formData.append('file', video, video.name);

    try {
      setIsUploading(true);
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadPercentage(percentCompleted);
        },
      });

      if (response.status === 200) {
        onUploadSuccess(); // Assuming this function is for handling successful upload in the parent component
      }
    } catch (error) {
      console.error('There was an error uploading the video!', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleButtonClick = () => {
    fileInput.current.click();
  };

  return (
    <Box
      display="flex"  
      justifyContent="center"  
      alignItems="center"  
      height="100%"  
    >
      <input 
        type="file"
        accept="video/*"
        hidden
        ref={fileInput}
        onChange={handleVideoChange}
      />
      {/* Use Stack to handle spacing between buttons */}
      <Stack direction="row" spacing={2} marginBottom={2}> 
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<CloudUploadIcon />} 
          onClick={handleButtonClick}
          disabled={isUploading}
        >
          Upload Video
        </Button>
        <Button 
          variant="contained" 
          color="secondary" 
          startIcon={<PlayArrowIcon />} 
          onClick={uploadVideo} 
          disabled={isUploading || !video}
        >
          Process
        </Button>
      </Stack>
      {isUploading && (
        <Box sx={{ width: '100%', marginTop: 2 }}>
          <LinearProgress variant="determinate" value={uploadPercentage} />
          <Box sx={{ textAlign: 'center', marginTop: 1 }}>
            {uploadPercentage}%
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default VideoUpload;
