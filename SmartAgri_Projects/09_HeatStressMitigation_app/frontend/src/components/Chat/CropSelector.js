import React from 'react';
import { Box, Select, MenuItem, Typography } from '@mui/material';

function CropSelector({ crop, handleCropChange, disabled }) {
    return (
      <Box className="controls-container">
        <Typography variant="p" className="crop-type-text">Crop Type:</Typography>
        <Select
          fullWidth
          value={crop}
          onChange={handleCropChange}
          variant="outlined"
          className="crop-select"
          disabled={disabled} // use the prop here
        >
          <MenuItem value="Barley">Barley</MenuItem>
          <MenuItem value="Corn">Corn</MenuItem>
          <MenuItem value="Canola">Canola</MenuItem>
          <MenuItem value="Durum Wheat">Durum Wheat</MenuItem>
          <MenuItem value="Fall Rye">Fall Rye</MenuItem>
          <MenuItem value="Flaxseed">Flaxseed</MenuItem>
          <MenuItem value="Lentils">Lentils</MenuItem>
          <MenuItem value="Mustard">Mustard</MenuItem>
          <MenuItem value="Oats">Oats</MenuItem>
          <MenuItem value="Peas">Peas</MenuItem>
          <MenuItem value="Soybeans">Soybeans</MenuItem>
          <MenuItem value="Spring Wheat">Spring Wheat</MenuItem>
          <MenuItem value="Winter Wheat">Winter Wheat</MenuItem>
        </Select>
      </Box>
    );
}

export default CropSelector;
