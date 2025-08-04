import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Message from '../components/Message';
import type { MessageType } from '../components/Message';
import ChatNav from '../components/ChatNav';
import useAuthFetch from '../hooks/useAuthFetch';
import useCurrentUserID from '../hooks/useCurrentUserID';

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    const { t } = useTranslation();
    
    const { data: message_data, loading, error } = useAuthFetch(`/message/chat-messages/full-info/${chat_id}`);
    const { id: currentUserId } = useCurrentUserID();
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    const messages: MessageType[] = (message_data as any[]).map((m) => ({
        sender_name: m.user.username,
        sender_pfp: m.user.pfp_url,
        content: m.content,
        sent_at: new Date(m.sent_at),
        is_own_message: m.sender_id == currentUserId,
    }));

    return (
        <>  
            <ChatNav
                chat_name="Chat Name"
                chat_pfp="https://example.com/chat-icon.jpg"
                is_group={false}
                member_count={2}
            />
            <main>
                <h1>{t('greeting')}</h1>
                <p>chat with id {chat_id} page placegolder text</p>
                {messages.map((message: MessageType, index: number) => (          
                    <Message key={index} message={{
                        sender_name: message.sender_name, 
                        sender_pfp: message.sender_pfp,
                        content: message.content, 
                        sent_at: message.sent_at,
                        is_own_message: message.is_own_message
                    }}/> ))}
            </main>
        </>
    );
}
