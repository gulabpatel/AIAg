import { GoogleMap, Marker } from '@react-google-maps/api';
import '../../App.css';

function Map({marker, setMarker, mapCenter, setMapCenter, onPlaceSelected }) {

    // const onMapClick = aysnc (e) => {
    //     const newMarker = { lat: e.latLng.lat(), lng: e.latLng.lng() };
    //     setMarker(newMarker);
    //     setMapCenter(newMarker);
    //     const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${newMarker.lat},${newMarker.lng}&key=AIzaSyC9AUBblaOS9QvGLcuNbR_iNSfwukn_d_0`);
    //     const data = await response.json();

    //     // Extract city name from response
    //     // Note: The actual structure of the response might be different, adjust accordingly
    //     const cityName = data.results[0].address_components.find(component => component.types.includes('locality')).long_name;
    //     console.log("City is: ", city);
    //     onPlaceSelected(newMarker);
    // };
    const onMapClick = async (e) => {
        const newMarker = { lat: e.latLng.lat(), lng: e.latLng.lng() };
        setMarker(newMarker);
        setMapCenter(newMarker);
        const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${newMarker.lat},${newMarker.lng}&key=AIzaSyC9AUBblaOS9QvGLcuNbR_iNSfwukn_d_0`);
        const data = await response.json();
        let cityName = '';
        for (let result of data.results) {
            const cityComponent = result.address_components.find(component => component.types.includes('locality'));
            if (cityComponent) {
                cityName = cityComponent.long_name;
                break;
            }
        }
    
        if (!cityName) {
            cityName = 'City not found';
        }
        console.log("City is: ", cityName);
        onPlaceSelected(newMarker, cityName);
    };

    return (
        <GoogleMap
            mapContainerClassName='map-container'
            center={mapCenter} // Use the dynamic map center
            zoom={7}
            onClick={onMapClick}
        >
            {marker && <Marker position={marker} />}
        </GoogleMap>
    );
}
  
export default Map;
  