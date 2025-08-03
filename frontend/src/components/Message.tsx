type MessageType = {
    sender_name: string;
    sender_pfp: string;
    content: string;
    sent_at: Date;
    is_own_message: boolean;
};

type Props = {
    message: MessageType;
};

export default function Message({ message }: Props) {
    return (
        <div className={`flex max-w-md mx-auto my-2 ${message.is_own_message ? "justify-end" : "justify-start"}`}>
            <div className={`flex items-start gap-4 p-3 rounded-lg shadow-sm text-left ${message.is_own_message ? "flex-row-reverse bg-blue-100" : "bg-gray-100 "}`}>
                <img
                    src={message.sender_pfp}
                    alt={`${message.sender_name}'s profile picture`}
                    className="w-12 h-12 rounded-full object-cover"
                />
                <div className="flex-1">
                    <div className="flex items-center justify-between">
                        <h2 className="font-semibold text-gray-900">{message.sender_name}</h2>
                        <time dateTime={message.sent_at.toISOString()} className="text-xs text-gray-500">
                            {message.sent_at.toLocaleString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
                        </time>
                    </div>
                    <p className="mt-1 text-gray-700 whitespace-pre-wrap">{message.content}</p>
                </div>
            </div>
        </div>
    );
}
