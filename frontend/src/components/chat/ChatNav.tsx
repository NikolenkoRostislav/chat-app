/*import ActivityIndicator from "./ActivityIndicator";*/
import useCurrentUserID from "../../hooks/useCurrentUserID";
import HomeButton from "../HomeButton";
import RouteButton from "../RouteButton";
import ChatLeaveButton from "./ChatLeaveButton";
import default_chat from '../../assets/default-chat.png';

type Props = {
    chat_id: string;
    creator_id: string;
    chat_name: string;
    chat_pfp: string;
    member_count: number;
};

export default function ChatNav({chat_name, chat_pfp, member_count, chat_id, creator_id}: Props) {
    const { id: user_id } = useCurrentUserID();

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
            <p className="text-sm text-gray-500">{member_count} members</p>
            { user_id != creator_id && <ChatLeaveButton chat_id={chat_id} user_id={user_id} /> }
        </nav>
    );
}
