import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Message from '../components/Message';
import ChatNav from '../components/ChatNav';

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    const { t } = useTranslation();
    const messages = [
        { 
            sender_name: "John Doe", 
            sender_pfp: "https://example.com/pfp.jpg",
            content: "Hello, this is a message!", 
            sent_at: new Date(),
            is_own_message: false
        },
        { 
            sender_name: "Don Jhoe", 
            sender_pfp: "https://example.com/pfp.jpg",
            content: "Hi, this is a different message!", 
            sent_at: new Date(),
            is_own_message: true
        },
        { 
            sender_name: "Don Jhoe", 
            sender_pfp: "https://example.com/pfp.jpg",
            content: "And this is a long message that should wrap properly across multiple lines to ensure it looks good in the chat interface. Let's see how it handles this text.", 
            sent_at: new Date(),
            is_own_message: true
        },
    ];

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
                {messages.map((message, index) => (               
                <Message key={index} message={message}/> ))}
            </main>
        </>
    );
}
