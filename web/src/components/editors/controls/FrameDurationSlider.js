import React from 'react';
import Typography from "@material-ui/core/Typography";
import Slider from "@material-ui/core/Slider";
import {debounce} from "lodash";

const FrameDurationSlider = ({frameDuration, onChange}) => {
    const callback = debounce((event, value) => {
        onChange(value);
    }, 500);
    return <div>
        <Typography id="discrete-slider-small-steps" gutterBottom>
            Frame delay
        </Typography>
        <Slider
            min={10}
            max={1000}
            step={10}
            defaultValue={frameDuration}
            onChange={callback}
            aria-labelledby="discrete-slider"
            valueLabelDisplay="auto"
        />
    </div>
};

export default FrameDurationSlider;