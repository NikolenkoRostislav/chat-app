import { useParams } from 'react-router-dom';
import Message from '../components/chat/Message';
import type { MessageType } from '../components/chat/Message';
import ChatNav from '../components/chat/ChatNav';
import useAuthFetch from '../hooks/useAuthFetch';
import useCurrentUserID from '../hooks/useCurrentUserID';
import MessageButton from '../components/chat/MessageButton';

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    
    const { data: message_data, loading, error } = useAuthFetch(`/message/chat-messages/full-info/${chat_id}`);
    const { data: chat_data } = useAuthFetch(`/chat/${chat_id}`);
    const { data: chat_member_data } = useAuthFetch(`/chat-member/user-memberships-count/${chat_id}`);
    const { id: currentUserId } = useCurrentUserID();
    
    if (error) return <p>Error: {error}</p>;
    if (loading || !chat_data || !chat_member_data || !chat_id) return <p>Loading...</p>;

    const messages: MessageType[] = (message_data as any[]).map((m) => ({
        sender_name: m.user.username,
        sender_pfp: m.user.pfp_url,
        content: m.content,
        sent_at: new Date(m.sent_at),
        is_own_message: m.sender_id == currentUserId,
    }));

    return (
        <div className="flex flex-col h-screen">  
            <ChatNav
                chat_id ={chat_id}
                chat_name={chat_data.name}
                chat_pfp={chat_data.icon_url}
                is_group={false}
                member_count={chat_member_data}
            />
            <main className="flex-1 flex flex-col max-w-3xl mx-auto p-4">
            {messages.length === 0 ? (
                <div className="flex-1 flex items-center justify-center">
                    <p className="text-gray-500 text-center">No messages yet</p>
                </div>
            ) : (
                <div className="flex-1 overflow-y-auto space-y-2">
                    {messages.map((message: MessageType, index: number) => (
                        <Message
                            key={index}
                            message={{
                                sender_name: message.sender_name,
                                sender_pfp: message.sender_pfp,
                                content: message.content,
                                sent_at: message.sent_at,
                                is_own_message: message.is_own_message,
                            }}
                        />
                    ))}
                </div>
            )}

            {chat_id && <MessageButton route={"/message/"} chat_id={chat_id} />}
        </main>
        </div>
    );
}
