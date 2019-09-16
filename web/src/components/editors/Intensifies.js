import React, {Component} from 'react'
import API from '../../api';
import debounce from 'lodash/debounce';
import Slider from "@material-ui/core/Slider";
import EditorCard from "./EditorCard";
import {Container} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";

class Intensifies extends Component {
    constructor(props) {
        super(props);
        this.state = {
            intensity: 7,
            emoji_id: this.props.id,
            url: null,
            name: 'Intensifies',
            loading: true
        }
    }

    componentDidMount() {
        API.post(`/api/v1/emoji/${this.state.emoji_id}/intensifies`, {
            intensity: this.state.intensity
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

    setIntensity = debounce((event, intensity) => {
        this.setState({loading: true});
        API.post(`/api/v1/emoji/${this.state.emoji_id}/intensifies`, {
            intensity: intensity
        }).then(resp => {
            const {url} = resp.data;
            this.setState({
                loading: false,
                intensity: intensity,
                url: API.defaults.baseURL + url
            });
        })
    }, 500);

    render() {
        const controls = (
            <Container>
                <Typography id="discrete-slider-small-steps" gutterBottom>
                    Intensity
                </Typography>
                <Slider
                    min={1}
                    max={20}
                    step={1}
                    defaultValue={this.state.intensity}
                    onChange={this.setIntensity.bind(this)}
                    aria-labelledby="discrete-slider"
                    valueLabelDisplay="auto"
                />
            </Container>
        );

        return <EditorCard loading={this.state.loading} name={this.state.name} url={this.state.url} controls={controls}/>
    }
}

export default Intensifies;