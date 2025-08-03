type MessageType = {
    sender_name: string;
    sender_pfp: string;
    content: string;
    sent_at: Date;
};

type Props = {
    message: MessageType;
};

export default function Message({ message }: Props) {
    return (
        <div className="message">
            <img src={message.sender_pfp} alt={`${message.sender_name}'s profile picture`} />
            <h2>{message.sender_name}</h2>
            <p>{message.content}</p>
            <time dateTime={message.sent_at.toLocaleTimeString()}>{message.sent_at.toLocaleString([], {hour: '2-digit', minute: '2-digit', hour12: false})}</time>
        </div>
    );
}
