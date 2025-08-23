import { useEffect, useMemo, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Message from '../components/chat/Message';
import type { MessageType } from '../components/chat/Message';
import ChatNav from '../components/chat/ChatNav';
import useAuthFetch from '../hooks/useAuthFetch';
import useCurrentUserID from '../hooks/useCurrentUserID';
import MessageButton from '../components/chat/MessageButton';
import { socket } from "../socket";

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    
    const { data: message_data, loading, error, refetch } = useAuthFetch(`/message/chat/${chat_id}`);
    const { data: chat_data } = useAuthFetch(`/chat/${chat_id}`);
    const { data: chat_member_data } = useAuthFetch(`/chat/member-count/${chat_id}`);
    const { id: current_user_id } = useCurrentUserID();

    useEffect(() => {
        if (!socket.connected) {
            socket.connect()
        } else {
            const token = localStorage.getItem("token");
            socket.emit("identify_user", {token});
        }

        const handleNewMessage = () => {
            refetch();
            console.log("received new message");
        };

        socket.on("new_message_received", handleNewMessage);

        return () => {
            socket.off("new_message_received", handleNewMessage);
        };
    }, []);

    const messages: MessageType[] = useMemo(() => (message_data || []).map((m: any) => ({
        sender_name: m.user.username,
        sender_pfp: m.user.pfp_url,
        content: m.content,
        sent_at: new Date(m.sent_at),
        is_own_message: m.sender_id == current_user_id,
    })), [message_data, current_user_id]);

    useEffect(() => {
        setTimeout(() => {
            messagesEndRef.current?.scrollIntoView({ behavior: "auto" });
        }, 1);
    }, [messages]);

    if (error) return <p>Error: {error}</p>;
    if (loading || !chat_data || !chat_member_data || !chat_id || !current_user_id) return <p>Loading...</p>;

    return (
        <div className="flex flex-col h-screen">  
            <ChatNav
                chat_id={chat_id}
                creator_id={chat_data.creator_id}
                chat_name={chat_data.name}
                chat_pfp={chat_data.icon_url}
                member_count={chat_member_data}
            />
            <main className="flex-1 flex flex-col max-w-3xl mx-auto p-4 overflow-y-auto">
                {messages.length === 0 ? (
                    <div className="flex-1 flex items-center justify-center">
                        <p className="text-gray-500 text-center">No messages yet</p>
                    </div>
                ) : (
                    <div className="flex-1 overflow-y-auto space-y-2 overflow-x-hidden">
                        {messages.map((message: MessageType, index: number) => (
                            <Message key={index} message={message}/>
                        ))}
                        <div ref={messagesEndRef}/>
                    </div>
                )}
                {chat_id && <MessageButton route={"/message/"} chat_id={chat_id} />}
            </main>
        </div>
    );
}
