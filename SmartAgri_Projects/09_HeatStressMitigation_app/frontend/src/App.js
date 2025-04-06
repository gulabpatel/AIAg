import './App.css';
import React, { useState } from 'react';
import { Button, Box, Container, Grid, Typography } from '@mui/material';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import CloseIcon from '@mui/icons-material/Close';
import { LoadScript } from '@react-google-maps/api';
import Search from './components/Search/Search';
import Map from './components/Map/Map';
import ChatBot from './components/Chat/ChatBot';
import WeeklyForecast from './components/WeeklyForecast/WeeklyForecast';
import TodayWeather from './components/TodayWeather/TodayWeather';
import { fetchWeatherData } from './api/OpenWeatherService';
import { transformDateFormat } from './utilities/DatetimeUtils';
import UTCDatetime from './components/Reusable/UTCDatetime';
import LoadingBox from './components/Reusable/LoadingBox';
import Logo from './assets/logo.webp';
import ErrorBox from './components/Reusable/ErrorBox';
import { ALL_DESCRIPTIONS } from './utilities/DateConstants';
import {
  getTodayForecastWeather,
  getWeekForecastWeather,
} from './utilities/DataUtils';

const libraries = ["places"];

const GOOGLE_MAPS_API_KEY="AIzaSyC9AUBblaOS9QvGLcuNbR_iNSfwukn_d_0";
function App() {
  const [marker, setMarker] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: 51.5072, lng: 0.1276 });
  const [todayWeather, setTodayWeather] = useState(null);
  const [todayForecast, setTodayForecast] = useState([]);
  const [weekForecast, setWeekForecast] = useState(null);
  const [weekForecastResponse, setWeekForecastResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const [isChatBotVisible, setIsChatBotVisible] = useState(false);

  // Function to toggle ChatBot visibility
  const toggleChatBot = () => {
    setIsChatBotVisible(!isChatBotVisible);
  };

  const onPlaceSelected = async (place, cityName) => {
    const location = place.geometry && place.geometry.location ? place.geometry.location : place;
    console.log(location);
    const newMarker = { 
      lat: typeof location.lat === 'function' ? location.lat() : location.lat, 
      lng: typeof location.lng === 'function' ? location.lng() : location.lng 
  };
    setMarker(newMarker);
    setMapCenter(newMarker);
    const latitude = newMarker.lat;
    const longitude = newMarker.lng;
    console.log(cityName);

    setIsLoading(true);

    const currentDate = transformDateFormat();
    const date = new Date();
    let dt_now = Math.floor(date.getTime() / 1000);

    try {
      const [todayWeatherResponse, weekForecastResponse] =
        await fetchWeatherData(latitude, longitude);
      console.log(todayWeatherResponse);
      console.log(weekForecastResponse);
      setWeekForecastResponse(weekForecastResponse);
      const all_today_forecasts_list = getTodayForecastWeather(
        weekForecastResponse,
        currentDate,
        dt_now
      );

      const all_week_forecasts_list = getWeekForecastWeather(
        weekForecastResponse,
        ALL_DESCRIPTIONS
      );
      setTodayForecast([...all_today_forecasts_list]);
      setTodayWeather({ city: cityName, ...todayWeatherResponse });
      setWeekForecast({
        city: cityName,
        list: all_week_forecasts_list,
      });
    } catch (error) {
      setError(true);
    }
    setIsChatBotVisible(true);
    setIsLoading(false);
  };

  return (
    <div>
    <Container className="app-container">
      <Grid container columnSpacing={2}>
        <Grid item xs={12}>
          <Box
           className="header-box"
           sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
          }}
           >
            <Box
              component="img"
              className="logo-img"
              alt="logo"
              src={Logo}
            />
            <UTCDatetime />
            <Box className='logo-box'>
              <Typography variant="h2" component="h2" className='logo-typography' sx={{fontFamily: "Poppins"}}>
                AgriWeather
              </Typography>
            </Box>
          </Box>
          <div className='App'>
          <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY} libraries={libraries}>
            <Search onPlaceSelected={onPlaceSelected} />
            <Map marker={marker} setMarker={setMarker} mapCenter={mapCenter} setMapCenter={setMapCenter} onPlaceSelected={onPlaceSelected} />
          </LoadScript>
          </div>
          
        </Grid>
  
        {isLoading ? (
          <Box className="loading-box">
            <LoadingBox value="1">
              <Typography
                variant="h3"
                component="h3"
                className="loading-typography"
                sx={{fontFamily: "Poppins"}}
              >
                Loading...
              </Typography>
            </LoadingBox>
          </Box>
        ) : error ? (
          <ErrorBox
            className="error-box"
            errorMessage="Something went wrong"
          />
        ) : todayWeather && todayForecast && weekForecast ? (
          <React.Fragment>
            <Grid item xs={12} md={todayWeather ? 6 : 12}>
              <TodayWeather data={todayWeather} forecastList={todayForecast} />
            </Grid>
            <Grid item xs={12} md={6}>
              <WeeklyForecast data={weekForecast} />
            </Grid>
          </React.Fragment>
        )
         : (
          <Box className="app-box">
            <Typography
              variant="h4"
              component="h4"
              className="app-typography"
              sx={{fontFamily: "Poppins"}}
            >
              Select your location and get weather insights for thriving crops!
            </Typography>
          </Box>
        )
        }

      </Grid>
    </Container>
      <div>
        <Button
        //  className='floating-button' 
         onClick={toggleChatBot}
         sx={{
          position: 'fixed',
          width: '60px',
          height: '60px',
          bottom: '20px',
          right: '20px',
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)',
          borderRadius: '50%',
          backgroundColor: '#f5f5f5',
          ':hover': {
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.3)',
            backgroundColor: '#e0e0e0'
          }
        }}
         >
          {isChatBotVisible ? <CloseIcon /> : <ChatBubbleOutlineIcon />}
        </Button>
        <ChatBot className={`chatbot-container ${isChatBotVisible ? 'visible' : 'hidden'}`} marker={marker} weekForecastResponse={weekForecastResponse} />
      </div>
    </div>

  );  
}

export default App;
