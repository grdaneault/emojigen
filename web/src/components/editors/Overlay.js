import React, {Component} from 'react'
import API from '../../api';
import debounce from 'lodash/debounce';
import EditorCard from "./EditorCard";
import {Container} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FrameDurationSlider from "./controls/FrameDurationSlider";
import PropTypes from "prop-types";
import {withStyles} from "@material-ui/styles";

const styles = {
    margin: {
        height: 30,
    },
};

class Overlay extends Component {
    constructor(props) {
        super(props);
        this.state = {
            overlay: "fire.gif",
            frameDuration: 50,
            emoji_id: this.props.id,
            url: null,
            name: 'Overlay',
            loading: true
        }
    }

    componentDidMount() {
        API.post(`/api/v1/emoji/${this.state.emoji_id}/overlay`, {
            overlay: this.state.overlay,
            frame_duration: this.state.frameDuration
        })
            .then(resp => {
                const {url, name} = resp.data;
                this.setState({
                    loading: false,
                    url: API.defaults.baseURL + url,
                    name
                });
            });
    }

    setOverlay = debounce((event) => {
        this.setState({loading: true});
        API.post(`/api/v1/emoji/${this.state.emoji_id}/overlay`, {
            overlay: event.target.value,
            frame_duration: this.state.frameDuration
        }).then(resp => {
            const {url, name} = resp.data;
            this.setState({
                loading: false,
                overlay: event.target.value,
                url: API.defaults.baseURL + url,
                name
            });
        })
    }, 500);

    setFrameDuration = (frameDuration) => {
        this.setState({loading: true});
        API.post(`/api/v1/emoji/${this.state.emoji_id}/overlay`, {
            overlay: this.state.overlay,
            frame_duration: frameDuration
        }).then(resp => {
            const {url} = resp.data;
            this.setState({
                loading: false,
                frameDuration: frameDuration,
                url: API.defaults.baseURL + url
            });
        })
    };

    render() {
        const { classes } = this.props;

        const controls = (
            <Container>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    Pattern
                </Typography>
                <Select onChange={this.setOverlay.bind(this)} value={this.state.overlay}>
                    <MenuItem value="fire.gif">Fire</MenuItem>
                    <MenuItem value="sparkle2.gif">Sparkle</MenuItem>
                    <MenuItem value="loving.gif">Hearts</MenuItem>
                </Select>
                <div className={classes.margin} />
                <FrameDurationSlider frameDuration={this.state.frameDuration} onChange={this.setFrameDuration} />
            </Container>
        );

        return <EditorCard loading={this.state.loading} name={this.state.name} url={this.state.url} controls={controls}/>
    }

}

Overlay.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Overlay);