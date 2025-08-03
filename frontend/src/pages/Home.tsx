import { useTranslation } from 'react-i18next';
import ChatButton from '../components/ChatButton';
import useAuthFetch from "../hooks/useAuthFetch";

export default function Home() {
    const { t } = useTranslation();
    type MembershipType = {
        chat_id: string;
        chat_name: string; 
        chat_pfp: string; 
        last_message: string; 
    };

    const { data: memberships, loading, error } = useAuthFetch("/chat-member/user-memberships/me");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            {memberships.map((membership: MembershipType, index: number) => (          
            <ChatButton key={index} chat_button={{
                chat_id: membership.chat_id,
                chat_name: `Chat ${membership.chat_id}`,
                chat_pfp: "https://example.com/chat.jpg",
                last_message: `Last message in Chat ${membership.chat_id}`
            }}/> ))}
        </main>
    );
}
