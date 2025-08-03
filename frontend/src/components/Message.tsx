type Props = {
    sender_name: string;
    sender_pfp: string;
    content: string;
    sent_at: Date;
};

export default function Message({ sender_name, sender_pfp, content, sent_at }: Props) {
    return (
        <div className="message">
            <img src={sender_pfp} alt={`${sender_name}'s profile picture`} />
            <h2>{sender_name}</h2>
            <p>{content}</p>
            <time dateTime={sent_at.toLocaleTimeString()}>{sent_at.toLocaleString([], {hour: '2-digit', minute: '2-digit', hour12: false})}</time>
        </div>
    );
}