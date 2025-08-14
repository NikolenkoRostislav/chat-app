import RouteButton from "./RouteButton";
import default_chat from '../assets/default-chat.png';

export type ChatButtonType = {
    chat_id: string;
    chat_name: string;
    chat_icon_url: string;
    last_message?: string;
};

type Props = {
    chat_button: ChatButtonType;
};

export default function ChatButton({ chat_button }: Props) {
    return (
        <RouteButton route={`chat/${chat_button.chat_id}`}>
            <div className="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer">
                <img 
                    src={chat_button.chat_icon_url} 
                    alt={`${chat_button.chat_name} chat icon`} 
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_chat;
                    }}
                    className="w-18 h-18 rounded-full object-cover border border-gray-300" 
                />
                <h2 className="text-lg font-semibold truncate">{chat_button.chat_name}</h2>
                {chat_button.last_message && <p className="text-sm text-gray-500 truncate">{chat_button.last_message}</p>}
            </div>
        </RouteButton>
    );
}