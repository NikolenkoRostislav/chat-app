import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Message from '../components/Message';
import ChatNav from '../components/ChatNav';

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    const { t } = useTranslation();

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
                <Message 
                    sender_name="John Doe" 
                    sender_pfp="https://example.com/pfp.jpg" 
                    content="Hello, this is a message!" 
                    sent_at={new Date()}
                />
            </main>
        </>
    );
}