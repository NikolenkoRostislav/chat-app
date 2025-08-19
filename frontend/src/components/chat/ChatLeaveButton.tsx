import { useNavigate } from "react-router-dom";
import useAuthDelete from "../../hooks/useAuthDelete";

type Props = {
    chat_id: string;
    user_id: string;
};

export default function ChatLeaveButton({chat_id, user_id}: Props) {
    const navigate = useNavigate();
    const { delete_func } = useAuthDelete();

    const onClick = async () => {
        const payload = { 
            chat_id,
            user_id,
        };

        try {
            await delete_func("/chat-member/remove-member", payload);
            navigate("/")
        } catch (err) {   
            alert("Failed to leave chat: " + err);
        }
    }

    return (
        <button 
            onClick={onClick}
            className="ml-auto text-red-500 cursor-pointer"
        > 
            Leave Chat
        </button>
    );
}
