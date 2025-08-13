import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';
import useAuthFetch from "../hooks/useAuthFetch";
import type { ChatButtonType } from '../components/ChatButton';

export default function Home() {
    const { t } = useTranslation();

    const { data: chats_data, loading, error } = useAuthFetch("/chat-member/chats/me");
    if (loading) return <p className="text-center text-gray-500 mt-6">Loading...</p>;
    if (error) return <p className="text-center text-gray-500 mt-6">Error: {error}</p>;

    const chat_buttons: ChatButtonType[] = (chats_data as any[]).map((c) => ({
        chat_id: c.id,
        chat_name: `${c.name}`,
        chat_icon_url: `${c.icon_url}`,
        last_message: `Last message in Chat ${c.id}`
    }));

    return (
        <main className="max-w-3xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-2">{t('greeting')}</h1>
            <p className="text-gray-600 mb-6">home page placegolder text</p>
            <div className="bg-white rounded-2xl shadow p-4 space-y-3">
            {chat_buttons.map((chat: ChatButtonType, index: number) => (          
                <ChatButton key={index} chat_button={{
                    chat_id: chat.chat_id,
                    chat_name: chat.chat_name,
                    chat_icon_url: chat.chat_icon_url,
                    last_message: chat.last_message
                }}/> ))}
            </div>
        </main>
    );
}
