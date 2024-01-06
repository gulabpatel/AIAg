import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const VideoDisplay = ({ uploadSuccessful, resetUpload }) => {
  const [frameSrc, setFrameSrc] = useState('');  // State for the frame image source
  const [objectCount, setObjectCount] = useState(0);  // State for the object count
  const [source, setSource] = useState(null);

  useEffect(() => {
    if (uploadSuccessful && !source) {
      if (!!window.EventSource) {
        const newSource = new EventSource('http://127.0.0.1:5000/stream');
        
        newSource.onmessage = (event) => {
          // Parse the JSON data to extract frame and count
          const data = JSON.parse(event.data);
          setFrameSrc(`data:image/jpeg;base64,${data.frame}`);
          setObjectCount(data.count);  // Set the new count
        };

        newSource.onerror = (err) => {
          console.error("EventSource failed:", err);
          newSource.close();
        };

        setSource(newSource);
      }
    }

    if (resetUpload && source) {
      source.close(); // Close the previous connection
      setSource(null);
      setFrameSrc(''); // Reset the frame source as well
      setObjectCount(0); // Reset the object count
    }
  }, [uploadSuccessful, resetUpload, source]);

  return (
    <div className="video-display-container">
      {frameSrc && (
        <div className="video-container">
          <img src={frameSrc} alt="Stream frame" className="stream-frame" />
        </div>
      )}
      
      <Card className="count-card" variant="outlined">
        <CardContent className='card-text'>
          {objectCount}
        </CardContent>
        <Typography variant="h6" component="div">
            Weed count
        </Typography>
      </Card>
    </div>
  );
};

export default VideoDisplay;
