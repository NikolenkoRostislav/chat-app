import ActivityIndicator from "./ActivityIndicator";
import RouteButton from "./RouteButton";

type Props = {
    chat_name: string;
    chat_pfp: string;
    is_group: boolean;
    member_count: number;
};

export default function Message({chat_name, chat_pfp, is_group, member_count}: Props) {
    return (
        <nav className="chat-nav">
            <RouteButton route="">
                <p>Home</p>
            </RouteButton>
            <img src={chat_pfp} alt={`${chat_name} chat icon`} />
            <h1>{chat_name}</h1>
            {is_group ? <p>{member_count} members</p> : <ActivityIndicator activity="online"/>}
        </nav>
    );
}