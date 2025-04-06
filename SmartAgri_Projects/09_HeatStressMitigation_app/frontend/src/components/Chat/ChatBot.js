import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button } from '@mui/material';
import { AppBar, Avatar, Toolbar, Typography } from '@mui/material';
import OnlineIndicator from '@mui/icons-material/FiberManualRecord'; // An icon for online status
import SendIcon from '@mui/icons-material/Send';
import CropSelector from './CropSelector';
import StageSelector from './StageSelector';
import '../../App.css'
import ProfilePic from '../../assets/weatherChat.png'


function ChatBot({ className, marker, weekForecastResponse }) {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { user: 'Bot', message: "Hello there! I'm AgriWeatherBot, your personal assistant for smarter farming. Let me know the crops you're growing and their stage, and I'll provide tailored agricultural tips based on the weather of your selected location. How can I assist you today?"},
    { user: 'Bot', type: 'crop-selector', message: 'Please select a crop.' },
    { user: 'Bot', type: 'stage-selector', message: 'Please select the stage of your crop.' }
  ]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [crop, setCrop] = useState('');
  const [stage, setStage] = useState('');

  const [showPredictiveButton, setShowPredictiveButton] = useState(false);
  const [isAnalysisButtonPressed, setIsAnalysisButtonPressed] = useState(false);
  const [showResetButton, setShowResetButton] = useState(false);

  const resetCrop = () => {
    setCrop('');
    setStage('');
    setChatHistory([{ user: 'Bot', message: 'Please select a crop and stage to begin.' }, { user: 'Bot', type: 'crop-selector' }, 
    { user: 'Bot', type: 'stage-selector' }]);
    setShowResetButton(false);
    setIsAnalysisButtonPressed(false);
  };


  const handleCropChange = e => {
    setCrop(e.target.value);
  };

  const handleStageChange = e => {
    setStage(e.target.value);
    setShowPredictiveButton(true);
    };
  
  const fetchPrediction = () => {
    setIsAnalysisButtonPressed(true);
    setIsBotTyping(true);
    setShowResetButton(true);
    fetch('http://127.0.0.1:5000/api/get-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        lat: marker.lat,
        lng: marker.lng,
        crop: crop,
        stage: stage,
        forecast: weekForecastResponse
      })
    })
    .then(response => response.json())
    .then(data => {
      setIsBotTyping(false);
      setChatHistory([...chatHistory, { user: 'You', message: `Selected crop: ${crop}` }, { user: 'You', message: `Selected stage: ${stage}` }, 
      { user: 'Bot', message: data.response}]);
      setShowPredictiveButton(false);
    })
    .catch(error => {
      console.error("Error fetching predictive analysis:", error);
      setIsBotTyping(false);
      setChatHistory([...chatHistory, { user: 'You', message: `Selected crop: ${crop}` }, { user: 'You', message: `Selected stage: ${stage}` },
      { user: 'Bot', message: 'Sorry, an error occurred. Please try again later.' }]);
      setShowPredictiveButton(false);
    });
  };
  
  const handleKeyPress = (event) => {
    if(event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevents the default action of the Enter key
      sendMessage();
    }
  };

const sendMessage = () => {
    if (message.trim()) {
      setChatHistory([...chatHistory, { user: 'You', message: message.trim() }]);
      setMessage('');
  
      setIsBotTyping(true); // bot starts "typing"
  
      fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message.trim() }) // send user's message to the server
      })
      .then(response => response.json())
      .then(data => {
        setIsBotTyping(false); // bot finished "typing"
        setChatHistory(prevChatHistory => [...prevChatHistory, { user: 'Bot', message: data.response }]);
      })
      .catch(error => {
        setIsBotTyping(false);
        console.error('Error sending message:', error);
        setChatHistory(prevChatHistory => [...prevChatHistory, { user: 'Bot', message: 'Error communicating with the server.' }]);
      });
    }
  };
  
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  return (
    <div className={className}>
    <AppBar position="static" className="appBar">
      <Toolbar className="toolbar">
        <Avatar src={ProfilePic} alt="ProfilePic" sx={{ marginRight: '10px' }} />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Typography variant="h6" color="inherit" sx={{ wordWrap: "break-word" }}>
            AgriWeatherBot
          </Typography>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <OnlineIndicator sx={{ color: '#32CD32', width: "10px", height: "10px" }} />
            <Typography variant="caption" color="inherit" sx={{ fontStyle: 'italic', marginLeft: '5px' }}>
              Online
            </Typography>
          </div>
        </div>
      </Toolbar>
    </AppBar>
      <Box className="chat-history">
        {chatHistory.map((chat, index) => {
        if (chat.type === 'crop-selector') {
            return (
                <div key={index} className="bot-message bot-selector-message">
                    <CropSelector crop={crop} handleCropChange={handleCropChange} disabled={isAnalysisButtonPressed} />
                </div>

            );
        }
        else if (chat.type === 'stage-selector') {
            return (
                <div>
                    <div key={index} className="bot-message bot-selector-message">
                        <StageSelector stage={stage} handleStageChange={handleStageChange} disabled={isAnalysisButtonPressed} />
                    </div>
                    {
                        showPredictiveButton && 
                        <Button
                         sx={{ alignSelf: 'center', marginTop: '10px', margin: '10px auto', display: 'block' }}
                         variant='outlined'
                         onClick={fetchPrediction}
                         >
                          Get Advice
                        </Button>
                    }
    
                </div>
                );
        } else {
            return (
            <div key={index} className={chat.user === 'You' ? 'user-message' : 'bot-message'}>
                <span dangerouslySetInnerHTML={{ __html: chat.message }}></span>
            </div>
            );
        }
        })}
        {isBotTyping && 
            <div className="bot-message">
            <div className="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            </div>
        }
        <div ref={messagesEndRef}></div>
      </Box>
      {
        showResetButton && 
        <Button onClick={resetCrop} variant="outlined" className="reset-crop-button">Reset Crop</Button>
      }
      <Box display="flex" className="input-box">
        <TextField
          fullWidth
          // sx={{ input: { color: 'black' } }}
          variant="outlined"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress} 
          placeholder="Type your message..."
        />
        <Button onClick={sendMessage}> <SendIcon /> </Button>
      </Box>
    </div>
  );
}

export default ChatBot;

