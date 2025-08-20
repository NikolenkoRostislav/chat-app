import { Routes, Route } from 'react-router';
import './App.css';

import Home from './pages/Home';
import Chat from './pages/Chat';
import ChatInfo from './pages/ChatInfo';
import Login from './pages/Login';
import Register from './pages/Register';
import UserMe from './pages/UserMe';
import UserInfo from './pages/UserInfo';
import useActivityPing from './hooks/useActivityPing';

export default function App() {
    useActivityPing();
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat/info/:chat_id" element={<ChatInfo />} />
            <Route path="/chat/:chat_id" element={<Chat />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/user/me" element={<UserMe />} />
            <Route path="/user/:username" element={<UserInfo />} />

            <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
    )
}
