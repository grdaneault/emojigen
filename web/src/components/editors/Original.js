import React, {Component} from 'react'
import API from '../../api';
import EditorCard from "./EditorCard";

class Original extends Component {
    constructor(props) {
        super(props);
        this.state = {
            intensity: 1,
            emoji_id: this.props.id,
            url: null,
            name: 'Original'
        }
    }

    componentDidMount() {
        API.get(`/api/v1/emoji/${this.state.emoji_id}`)
            .then(resp => {
                const {url, name} = resp.data;
                console.log(API.defaults.baseURL + url);
                this.setState({url: API.defaults.baseURL + url, name})
            });
    }

    render() {
        return <EditorCard name={this.state.name} url={this.state.url}/>
    }
}

export default Original;