import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';

export default function Home() {
    const { t } = useTranslation();
    const chats = [
        { 
            chat_id: "1", 
            chat_name: "Chat One", 
            chat_pfp: "https://example.com/chat1.jpg", 
            last_message: "Last message in Chat One" 
        },
        { 
            chat_id: "2", 
            chat_name: "Chat Two", 
            chat_pfp: "https://example.com/chat2.jpg", 
            last_message: "Last message in Chat Two" 
        },
        { 
            chat_id: "3", 
            chat_name: "Chat Three", 
            chat_pfp: "https://example.com/chat3.jpg", 
            last_message: "Last message in Chat Three" 
        },
    ];

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            {chats.map((chat, index) => (               
            <ChatButton key={index} chat_button={chat}/> ))}
        </main>
    );
}
