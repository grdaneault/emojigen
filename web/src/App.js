import React from 'react';
import {BrowserRouter as Router, Route, Link} from "react-router-dom"
import EmojiDropper from './components/EmojiDropper'
import EmojiEditor from "./components/EmojiEditor";
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    <Link to="/" className="App-link">EmojiGen</Link>
                </header>
            </div>
            <div className="Body">
                <Route path="/" exact component={EmojiDropper} />
                <Route path="/editor/:id" component={EmojiEditor} />
            </div>
        </Router>
    );
}

export default App;
