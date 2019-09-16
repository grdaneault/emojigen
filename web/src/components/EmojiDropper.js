import React, {Component, useMemo} from 'react'
import Dropzone from 'react-dropzone'
import API from '../api';
import axios from 'axios'
import {withRouter} from 'react-router-dom';

const baseStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    borderWidth: 2,
    borderRadius: 5,
    borderColor: '#dadada',
    borderStyle: 'dashed',
    backgroundColor: '#fafafa',
    color: '#bdbdbd',
    outline: 'none',
    transition: 'border .24s ease-in-out'
};

const activeStyle = {
    borderColor: '#2196f3'
};

const acceptStyle = {
    borderColor: '#00e676'
};

const rejectStyle = {
    borderColor: '#ff1744'
};

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


        return <div className="Drop-Zone">
            <Dropzone onDrop={this.onDrop} accept="image/*">
                {({
                      getRootProps,
                      getInputProps,
                      isDragActive,
                      isDragAccept,
                      isDragReject
                  }) => {

                    const style = useMemo(() => ({
                        ...baseStyle,
                        ...(isDragActive ? activeStyle : {}),
                        ...(isDragAccept ? acceptStyle : {}),
                        ...(isDragReject ? rejectStyle : {})
                    }), [
                        isDragActive,
                        isDragReject
                    ]);

                    return (
                        <section>
                            <div {...getRootProps({style})}>
                                <input {...getInputProps()} />
                                <p>Upload an image file</p>
                                <p>It will automatically be resized to 128x128px</p>
                            </div>
                        </section>
                    )
                }}

            </Dropzone>

        </div>
    }
}

export default withRouter(EmojiDropper);