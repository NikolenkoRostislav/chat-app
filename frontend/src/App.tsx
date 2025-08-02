import { Routes, Route } from 'react-router';
import './App.css';

import Home from './pages/Home';
import Chat from './pages/Chat';

export default function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat/:chat_id" element={<Chat />} />
        </Routes>
    )
}
