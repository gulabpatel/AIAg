import React from 'react';
import { Autocomplete } from '@react-google-maps/api';
import { useRef } from 'react';
import '../../App.css'

const Search = ({ onPlaceSelected }) => {

    const autocompleteRef = useRef(null);

    const onPlaceChanged = () => {
        if (autocompleteRef.current) {
            const place = autocompleteRef.current.getPlace();
            if (place && place.geometry && place.geometry.location) {
                onPlaceSelected(place, place.name);
            }
        }
    };

    return (
        <Autocomplete
            onLoad={(autocomplete) => (autocompleteRef.current = autocomplete)}
            onPlaceChanged={onPlaceChanged}
        >
            <input
                type="text"
                placeholder="Enter a location"
                className='search-bar'
            />
        </Autocomplete>
    );
};

export default Search;