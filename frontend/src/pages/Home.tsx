import { useState } from "react";
import useAuthFetch from "../hooks/useAuthFetch";
import ChatButton from '../components/home/ChatButton';
import UserInfoButton from '../components/home/UserInfoButton';
import ChatCreateButton from '../components/home/ChatCreateButton';
import ChatCreateMenu from '../components/home/ChatCreateMenu';
import LogoutButton from '../components/home/LogoutButton'
import type { ChatButtonType } from '../components/home/ChatButton';
import RouteButton from "../components/general/RouteButton";
import telegram_logo from '../assets/telegram-logo.png';

export default function Home() {
    const [chatCreationMenuOpen, setChatCreationMenuOpen] = useState(false);
    const { data: chats_data, loading, error } = useAuthFetch("/user/chats/me");
    if (loading) return <p className="text-center text-gray-500 mt-6">Loading...</p>;
    if (error) return <p className="text-center text-gray-500 mt-6">Error: {error}</p>;

    const chat_buttons: ChatButtonType[] = (chats_data as any[]).map((c) => ({
        chat_id: c.id,
        chat_name: `${c.name}`,
        chat_icon_url: `${c.icon_url}`,
        last_message: `Last message in Chat ${c.id}`
    }));

    return (
        <>  
            <nav className="flex items-center justify-between px-4 py-2 bg-white shadow-sm border-b sticky top-0 z-10">
                <UserInfoButton />
                <LogoutButton />
            </nav>
            <main className="max-w-3xl mx-auto p-4"> 
                <div className="bg-white rounded-2xl shadow p-4 space-y-3">
                {chat_buttons.map((chat: ChatButtonType, index: number) => (          
                    <ChatButton key={index} chat_button={{
                        chat_id: chat.chat_id,
                        chat_name: chat.chat_name,
                        chat_icon_url: chat.chat_icon_url,
                        last_message: chat.last_message
                    }}/> ))}
                    <ChatCreateButton setChatCreationMenuOpen={setChatCreationMenuOpen}/>
                </div>
                {chatCreationMenuOpen && <ChatCreateMenu setChatCreationMenuOpen={setChatCreationMenuOpen} />}
            </main>
            <footer className="fixed bottom-0 left-0 w-full bg-white border-t shadow-md p-3 flex items-center justify-between">
                <span className="text-sm text-gray-500">
                    Chat App by <span className="font-medium">Rostislav Nikolenko</span>
                </span>
                <RouteButton route="/telegram_link">
                    <img src={telegram_logo} alt="Telegram account link button" className="w-8 h-8 hover:opacity-80 transition" />
                </RouteButton>
            </footer>
        </>
    );
}
