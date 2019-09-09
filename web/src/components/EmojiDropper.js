import React, {Component} from 'react'
import Dropzone from 'react-dropzone'
import API from '../api';
import axios from 'axios'
import { withRouter } from 'react-router-dom';

class EmojiDropper extends Component {
    constructor(props) {
        super(props);

        this.state = {
            files: [],
        };
    }

    onDrop = (files) => {
        const uploads = files.map(image => {
            console.log("dropped!");
            const formData = new FormData();
            formData.append("emoji", image);
            return API.post("/api/v1/emoji", formData).then(resp => {
                console.log("Emoji uploaded", resp);
                this.props.history.push(`/editor/${resp.data.id}`);
            });
        });
        axios.all(uploads).then(() => {
            console.log('finished uploads');
        })
    };

    render() {

        return <div>
            <Dropzone onDrop={this.onDrop}>
                {({getRootProps, getInputProps}) => (
                    <section>
                        <div {...getRootProps()}>
                            <input {...getInputProps()} />
                            <p>Upload an emoji</p>
                        </div>
                    </section>
                )}
            </Dropzone>

        </div>
    }
}

export default withRouter(EmojiDropper);