import RouteButton from "./RouteButton";

export type ChatButtonType = {
    id: string;
    name: string;
    icon_url: string;
    last_message?: string;
};

type Props = {
    chat_button: ChatButtonType;
};

export default function ChatButton({ chat_button }: Props) {
    return (
        <RouteButton route={`chat/${chat_button.id}`}>
            <div className="chat-button">
                <img src={chat_button.icon_url} alt={`${chat_button.name} chat icon`} />
                <h2>{chat_button.name}</h2>
                {chat_button.last_message && <p className="last-message">{chat_button.last_message}</p>}
            </div>
        </RouteButton>
    );
}