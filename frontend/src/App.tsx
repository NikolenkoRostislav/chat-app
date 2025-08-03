import { Routes, Route } from 'react-router';
import './App.css';

import Home from './pages/Home';
import Chat from './pages/Chat';
import Login from './pages/Login';
import Register from './pages/Register';

export default function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat/:chat_id" element={<Chat />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
    )
}
