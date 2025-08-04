import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';
import useAuthFetch from "../hooks/useAuthFetch";
import type { ChatButtonType } from '../components/ChatButton';

export default function Home() {
    const { t } = useTranslation();

    const { data: chats, loading, error } = useAuthFetch("/chat-member/chats/me");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            {chats.map((chat: ChatButtonType, index: number) => (          
            <ChatButton key={index} chat_button={{
                id: chat.id,
                name: `${chat.name}`,
                icon_url: `${chat.icon_url}`,
                last_message: `Last message in Chat ${chat.id}`
            }}/> ))}
        </main>
    );
}
