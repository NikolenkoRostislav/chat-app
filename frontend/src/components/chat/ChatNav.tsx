/*import ActivityIndicator from "./ActivityIndicator";*/
import useAuthDelete from "../../hooks/useAuthDelete";
import useCurrentUserID from "../../hooks/useCurrentUserID";
import { useNavigate } from "react-router-dom";
import HomeButton from "../HomeButton";
import RouteButton from "../RouteButton";
import default_chat from '../../assets/default-chat.png';

type Props = {
    chat_id: string;
    chat_name: string;
    chat_pfp: string;
    is_group: boolean;
    member_count: number;
};

export default function ChatNav({chat_name, chat_pfp, /*is_group,*/ member_count, chat_id}: Props) {
    const navigate = useNavigate();
    const { delete_func } = useAuthDelete();
    const { id: user_id } = useCurrentUserID();

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
        <nav className="flex items-center gap-4 px-4 py-2 bg-white shadow-sm border-b sticky top-0 z-10">
            <HomeButton />
            <RouteButton route={`/chat/info/${chat_id}`}>
                <img 
                    src={chat_pfp} 
                    alt={`${chat_name} chat icon`} 
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_chat;
                    }}
                    className="w-12 h-12 rounded-full object-cover"
                />
            </RouteButton>
            <h1>{chat_name}</h1>
            {/*is_group ? <p className="text-sm text-gray-500">{member_count} members</p> : <ActivityIndicator activity="online"/>*/}
            <p className="text-sm text-gray-500">{member_count} members</p>
            <button 
                onClick={onClick}
                className="ml-auto text-red-500 cursor-pointer"
            > 
                Leave Chat
            </button>
        </nav>
    );
}
