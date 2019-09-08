import React, { Component, Fragment } from 'react'
import Dropzone from 'react-dropzone'


class EmojiDropper extends Component {
    constructor(props) {
        super(props)

        this.state = {
            files: [],
        };
    }

    render() {

        const previewStyle = {
            display: 'inline',
            width: 100,
            height: 100,
        };

        return <div>
            <Dropzone onDrop={this.onDrop} accept="image/*">
                {({getRootProps, getInputProps}) => (
                    <section>
                        <div {...getRootProps()}>
                            <input {...getInputProps()} />
                            <p>Drag some emoji here!</p>
                        </div>
                    </section>
                )}
            </Dropzone>

            {this.state.files.length > 0 &&
            <Fragment>
                <h3>Previews</h3>
                {this.state.files.map((file) => (
                    <img
                        alt="Preview"
                        key={file.preview}
                        src={file.preview}
                        style={previewStyle}
                    />
                ))}
            </Fragment>
            }
        </div>
    }

    onDrop = (files) => {
        console.log(files);
        this.setState({
            files: this.state.files.concat(files),
        });
    }
}

export default EmojiDropper