import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import useAuthFetch from '../hooks/useAuthFetch';
import useCurrentUserID from '../hooks/useCurrentUserID';
import HomeButton from '../components/HomeButton';
import ChatMember from '../components/chat_info/ChatMember';
import ChatMemberButton from '../components/chat_info/ChatMemberButton';
import type { ChatMemberType } from '../components/chat_info/ChatMember';
import default_chat from '../assets/default-chat.png';

export default function ChatInfo() {
    const { chat_id } = useParams<{ chat_id: string }>();

    if (!chat_id) return <p className="text-center mt-10">No chat id provided.</p>;

    const { id: current_user_id } = useCurrentUserID();
    const { data: chat, loading, error: chat_error } = useAuthFetch(`/chat/${chat_id}`);
    const { data: member_data, error: member_error } = useAuthFetch(`/chat-member/user-memberships/${chat_id}`);
    const [is_creator, setIsCreator] = useState(false);

    useEffect(() => {
        if (chat) {
            setIsCreator(current_user_id === chat.creator_id);
        }
    }, [chat, current_user_id]);

    if (loading) return <p className="text-center mt-10">Loading chat data...</p>;
    if (chat_error || member_error) return <p>Error: {chat_error || member_error}</p>;
    if (!chat) return <p>Chat not found.</p>;

    const members: ChatMemberType[] = (member_data ?? []).map((m: any) => ({
        member_id: m.id,
        user_id: m.user_id,
    }));

    return (
        <>
            <nav className="m-4">
                <HomeButton />
            </nav>
            <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
                <img 
                    src={chat.icon_url} 
                    alt="Chat icon" 
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_chat;
                    }}
                    className="w-32 h-32 rounded-full mx-auto mb-4" 
                />
                <h1 className="text-2xl font-bold mb-4 text-center">{chat.name}</h1>
                <p><strong>Members:</strong></p>
                <div>
                    {members.map((member: ChatMemberType, index: number) => (
                        <ChatMember
                            key={index}
                            member={{
                                member_id: member.member_id,
                                user_id: member.user_id,
                                chat_id: chat_id,
                                show_delete_button: is_creator,
                            }}
                        />
                    ))}
                </div>
                {is_creator && <ChatMemberButton chat_id={chat_id} />}
            </main>
        </>
    );
}
