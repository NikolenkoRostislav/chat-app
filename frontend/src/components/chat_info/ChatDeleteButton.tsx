import { useNavigate } from "react-router-dom";
import useAuthDelete from "../../hooks/useAuthDelete";

type Props = {
    chat_id: string;
};

export default function ChatDeleteButton({chat_id}: Props) {
    const navigate = useNavigate();
    const { delete_func } = useAuthDelete();

    const onClick = async () => {
        const confirm = prompt(`Are you sure you want to delete this chat?\n\nType "DELETE" to confirm: `);
        if (confirm != "DELETE") {
            return;
        }
        try {
            await delete_func(`/chat/delete/${chat_id}`, []);
            navigate("/")
        } catch (err) {   
            alert("Failed to delete chat: " + err);
        }
    }

    return (
        <button 
            onClick={onClick}
            className="text-red-500 cursor-pointer absolute bottom-0 right-0"
        > 
            Delete Chat
        </button>
    );
}
