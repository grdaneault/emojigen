import React, {Component} from 'react'
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/styles';
import API from '../../api';
import debounce from 'lodash/debounce';
import Slider from "@material-ui/core/Slider";
import EditorCard from "./EditorCard";
import Typography from "@material-ui/core/Typography";
import {Container} from "@material-ui/core";
import ColorPicker from 'material-ui-color-picker'

const styles = {
    margin: {
        height: 30,
    },
};

class Party extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            tolerance: 10,
            target_color: '#000000',
            emoji_id: this.props.id,
            url: null,
            name: 'Party'
        }
    }

    componentDidMount() {
        API.post(`/api/v1/emoji/${this.state.emoji_id}/party`, {
            tolerance: this.state.tolerance,
            target_color: this.state.target_color
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

    setTolerance = debounce((event, tolerance) => {
        this.setState({loading: true});
        API.post(`/api/v1/emoji/${this.state.emoji_id}/party`, {
            tolerance: tolerance,
            target_color: this.state.target_color
        }).then(resp => {
            const {url} = resp.data;
            this.setState({
                loading: false,
                tolerance: tolerance,
                url: API.defaults.baseURL + url
            });
        })
    }, 500);

    setTargetColor = debounce((target_color) => {
        if (!target_color) {
            // closing the widget seems to send undefined, don't do anything with that event.
            return;
        }

        this.setState({loading: true});
        API.post(`/api/v1/emoji/${this.state.emoji_id}/party`, {
            tolerance: this.state.tolerance,
            target_color: target_color
        }).then(resp => {
            const {url} = resp.data;
            this.setState({
                loading: false,
                target_color: target_color,
                url: API.defaults.baseURL + url
            });
        })
    }, 500);

    render() {
        const { classes } = this.props;

        const controls = (
            <Container>
                <Typography id="color-replace-label" gutterBottom>
                    Color to replace
                </Typography>
                <ColorPicker
                    name='color'
                    defaultValue='#000000'
                    onChange={this.setTargetColor.bind(this)}
                />
                <div className={classes.margin} />
                <Typography id="tolerance-label" gutterBottom>
                    Match Tolerance
                </Typography>
                <Slider
                    min={1}
                    max={500}
                    step={5}
                    defaultValue={this.state.tolerance}
                    onChange={this.setTolerance.bind(this)}
                    aria-labelledby="tolerance-label"
                    valueLabelDisplay="auto"
                />
            </Container>
        );

        return <EditorCard loading={this.state.loading} name={this.state.name} url={this.state.url} controls={controls}/>
    }
}

Party.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Party);