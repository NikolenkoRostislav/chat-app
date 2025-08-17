import RouteButton from '../RouteButton';
import default_pfp from '../../assets/default-pfp.png';

export type MessageType = {
    sender_name: string;
    sender_pfp: string;
    content: string;
    sent_at: Date;
    is_own_message: boolean;
};

type Props = {
    message: MessageType;
};

function insertZeroWidth(word: string, limit: number) {
    for (let i = limit; i < word.length; i += limit) {
        word =  word.slice(0, i) + "\u200B" + word.slice(i);
    }
    return word;
}

function breakLongWords(text: string, limit = 30) {
    return text
        .split(' ')
        .map(word => insertZeroWidth(word, limit))
        .join(' ');
}

export default function Message({ message }: Props) {
    return (
        <div className={`flex max-w-md mx-auto my-2 ${message.is_own_message ? "justify-end" : "justify-start"}`}>
            <div className={`flex items-start gap-4 p-3 rounded-lg shadow-sm text-left ${message.is_own_message ? "flex-row-reverse bg-blue-100" : "bg-gray-100 "}`}>
                <RouteButton route={message.is_own_message ? "/user/me" : `/user/${message.sender_name}`}>
                    <img
                        src={message.sender_pfp}
                        alt={`${message.sender_name}'s profile picture`}
                        onError={(e) => {
                            const img = e.target as HTMLImageElement;
                            img.onerror = null;
                            img.src = default_pfp;
                        }}
                        className="w-12 h-12 rounded-full object-cover"
                    />
                </RouteButton>
                <div className="flex-1">
                    <div className="flex items-center justify-between">
                        <h2 className="font-semibold text-gray-900">{message.sender_name}</h2>
                        <time dateTime={message.sent_at.toISOString()} className="text-xs text-gray-500">
                            {message.sent_at.toLocaleString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
                        </time>
                    </div>
                    <p className="mt-1 text-gray-700 whitespace-pre-wrap break-words">{breakLongWords(message.content)}</p>
                </div>
            </div>
        </div>
    );
}
