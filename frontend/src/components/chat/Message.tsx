import RouteButton from '../general/RouteButton';
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
        <div className={`flex max-w-md mx-auto my-2 ${message.is_own_message ? "justify-end mr-5 ml-15" : "justify-start ml-5 mr-15"}`}>
            <div className={`flex items-start gap-4 p-3 rounded-lg shadow-sm text-left relative
                ${message.is_own_message ? "flex-row-reverse bg-blue-100" : "bg-gray-100"}`}>
                <div className="relative">
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
                    <time 
                        dateTime={message.sent_at.toISOString()} 
                        className={"text-xs text-gray-500 absolute left-1/2 -translate-x-1/2"}
                    >
                        {message.sent_at.toLocaleString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
                    </time>
                </div>
                <div className="flex-1 flex flex-col relative">
                    <h2 className={`font-semibold text-gray-900 ${message.is_own_message ? "text-right" : "text-left"}`}>{message.sender_name}</h2>
                    <p className="mt-1 text-gray-700 whitespace-pre-wrap break-words">{breakLongWords(message.content)}</p>
                </div>
                <div className={`absolute bottom-[-1px] bg-black/8 w-3 h-0.5 ${message.is_own_message ? "-right-2" : "-left-2"}`} />
                <div className={`absolute bottom-0 border-l-15 translate-y-0.4
                    ${message.is_own_message 
                        ? "-right-2 border-t-15 border-t-transparent border-blue-100" 
                        : "-left-2 border-b-15 border-gray-100 border-l-transparent"
                    }
                `}/>
            </div>
        </div>
    );
}

