import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';
import useAuthFetch from "../hooks/useAuthFetch";
import type { ChatButtonType } from '../components/ChatButton';

export default function Home() {
    const { t } = useTranslation();

    const { data: chats_data, loading, error } = useAuthFetch("/chat-member/chats/me");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    const chat_buttons: ChatButtonType[] = (chats_data as any[]).map((c) => ({
        chat_id: c.id,
        chat_name: `${c.name}`,
        chat_icon_url: `${c.icon_url}`,
        last_message: `Last message in Chat ${c.id}`
    }));

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            {chat_buttons.map((chat: ChatButtonType, index: number) => (          
            <ChatButton key={index} chat_button={{
                chat_id: chat.chat_id,
                chat_name: chat.chat_name,
                chat_icon_url: chat.chat_icon_url,
                last_message: chat.last_message
            }}/> ))}
        </main>
    );
}
