import React from 'react';
import { Box, Select, MenuItem, Typography } from '@mui/material';

function StageSelector({ stage, handleStageChange, disabled }) {
    return (
      <Box className="controls-container">
        <Typography variant="p" className="crop-type-text">Crop Stage:</Typography>
        <Select
          fullWidth
          value={stage}
          onChange={handleStageChange}
          variant="outlined"
          className="crop-select"
          disabled={disabled} // use the prop here
        >
          <MenuItem value="Soil Preperation">Soil Preperation</MenuItem>
          <MenuItem value="Sowing">Sowing</MenuItem>
          <MenuItem value="Irrigation">Irrigation</MenuItem>
          <MenuItem value="Weeding">Weeding</MenuItem>
          <MenuItem value="Fertilizing">Fertilizing</MenuItem>
          <MenuItem value="Harvesting">Harvesting</MenuItem>
        </Select>
      </Box>
    );
}

export default StageSelector;
