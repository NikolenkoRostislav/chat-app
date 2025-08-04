import RouteButton from "./RouteButton";

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
            <div className="chat-button">
                <img src={chat_button.chat_icon_url} alt={`${chat_button.chat_name} chat icon`} />
                <h2>{chat_button.chat_name}</h2>
                {chat_button.last_message && <p className="last-message">{chat_button.last_message}</p>}
            </div>
        </RouteButton>
    );
}