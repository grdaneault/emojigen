import React from 'react';
import EmojiDropper from './components/EmojiDropper'
import logo from './logo.svg';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                EmojiGen
            </header>
            <EmojiDropper/>
        </div>
    );
}

export default App;
