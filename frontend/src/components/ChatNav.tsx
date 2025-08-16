/*import ActivityIndicator from "./ActivityIndicator";*/
import HomeButton from "./HomeButton";
import default_chat from '../assets/default-chat.png';

type Props = {
    chat_name: string;
    chat_pfp: string;
    is_group: boolean;
    member_count: number;
};

export default function ChatNav({chat_name, chat_pfp, /*is_group,*/ member_count}: Props) {
    return (
        <nav className="flex items-center gap-4 px-4 py-2 bg-white shadow-sm border-b sticky top-0 z-10">
            <HomeButton />
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
            <h1>{chat_name}</h1>
            {/*is_group ? <p className="text-sm text-gray-500">{member_count} members</p> : <ActivityIndicator activity="online"/>*/}
            <p className="text-sm text-gray-500">{member_count} members</p>
        </nav>
    );
}
