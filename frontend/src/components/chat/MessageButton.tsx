import { useState, useEffect, useRef } from "react";
import useAuthPost from "../../hooks/useAuthPost";

type Props = {
    route: string;
    chat_id: string;
};

export default function MessageButton({ route, chat_id }: Props) {
    const { post, loading } = useAuthPost();
    const [message, setMessage] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!message.trim()) {
            alert("Message cannot be empty");
            return;
        }

        const payload = { content: message, chat_id };
        try {
            await post(route, payload);
            setMessage("");
        } catch (err) { 
            alert("Failed to send message: " + err);
        }
    };

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [message]);

    return (
        <form onSubmit={handleSend} className="flex flex-row gap-4">
            <textarea
                ref={textareaRef}
                value={message}
                onChange={e => setMessage(e.target.value)}
                required
                className="flex-1 p-2 rounded border resize-none overflow-hidden focus:outline-none focus:ring-2 focus:ring-blue-400"
                rows={1}
                placeholder="..."
            />

            <button 
                type="submit" 
                className="flex-none bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-blue-600 disabled:opacity-50" 
                disabled={loading}
            >
                ➤
            </button>
        </form>
    );
}