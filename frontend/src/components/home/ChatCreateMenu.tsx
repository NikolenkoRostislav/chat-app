import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PopupMenu from "../general/PopupMenu";
import useAuthPost from "../../hooks/useAuthPost";
import useCurrentUserID from "../../hooks/useCurrentUserID";
import { socket } from "../../socket";

type Props = {
    setChatCreationMenuOpen: (open: boolean) => void;
};

export default function ChatCreateMenu({setChatCreationMenuOpen}: Props) {
    const [chat_name, setChatName] = useState("");
    const [icon_url, setIconUrl] = useState("");
    const { post: create_post } = useAuthPost();
    const { post: add_post } = useAuthPost();
    const {id: user_id} = useCurrentUserID();

    const navigate = useNavigate();

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!chat_name.trim()) {
            alert("Chat name cannot be empty");
            return;
        }

        const chat_create_payload = {
            name: chat_name,
            icon_url,
        };

        try {
            const data = await create_post("/chat/", chat_create_payload);
            const member_add_payload = {
                user_id,
                chat_id: data.id,
            }
            await add_post("/chat-member/join", member_add_payload);
            socket.connect();
            navigate(`/chat/${data.id}`);
        } catch (err) {
            alert("Chat creation failed: " + err);
        }
    }

    return (
        <PopupMenu setMenuOpen={setChatCreationMenuOpen}>
            <h1 className="text-2xl font-semibold mb-4">Create New Chat</h1>
            <form onSubmit={onSubmit}>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Chat Name</label>
                    <input 
                    type="text" 
                    value={chat_name} 
                    onChange={e => setChatName(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg" 
                    placeholder="Enter chat name" 
                    required
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Chat Icon URL</label>
                    <input 
                    type="text" 
                    value={icon_url} 
                    onChange={e => setIconUrl(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg" 
                    placeholder="Enter chat icon url" 
                    required
                    />
                </div>
                <button
                    type="submit"
                    className="mt-5 w-full bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Create Chat
                </button>
                </form>

        </PopupMenu>
    );
}