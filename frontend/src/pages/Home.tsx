import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';
import useAuthFetch from "../hooks/useAuthFetch";

export default function Home() {
    const { t } = useTranslation();

    type ChatType = {
        id: string;
        name: string; 
        icon_url: string; 
        last_message: string; 
    };

    const { data: chats, loading, error } = useAuthFetch("/chat-member/chats/me");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            {chats.map((chat: ChatType, index: number) => (          
            <ChatButton key={index} chat_button={{
                chat_id: chat.id,
                chat_name: `${chat.name}`,
                chat_pfp: `${chat.icon_url}`,
                last_message: `Last message in Chat ${chat.id}`
            }}/> ))}
        </main>
    );
}
