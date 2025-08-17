import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuthPost from "../../hooks/useAuthPost";
import useCurrentUserID from "../../hooks/useCurrentUserID";

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

    const onClose = () => {
        setChatCreationMenuOpen(false);
    }

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

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
            navigate(`/chat/${data.id}`);
        } catch (err) {
            alert("Chat creation failed: " + err);
        }
    }

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
            <div className="bg-white w-3/5 max-w-2xl h-2.5/5 p-6 rounded-2xl shadow-lg">
                <div className="flex justify-end">
                    <button onClick={onClose} className="w-10 h-10 rounded-full object-cover border border-gray-300 cursor-pointer hover:bg-gray-100">
                        <strong>X</strong>
                    </button>
                </div>
                <div className="mt-4">
                    <h1 className="text-2xl font-semibold mb-4">Create New Chat</h1>
                    <form>
                        <div className="mb-10"/>
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Chat Name</label>
                            <input 
                                type="text" 
                                value={chat_name} 
                                onChange={e => setChatName(e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-lg" 
                                placeholder="Enter chat name" 
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
                            />
                        </div>
                        <div className="mb-10" />
                            
                        <button
                            type="submit"
                            className="w-full bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors"
                            onClick={onSubmit}
                        >
                            Create Chat
                        </button>
                    </form>
                </div> 
            </div>
        </div>
    );
}