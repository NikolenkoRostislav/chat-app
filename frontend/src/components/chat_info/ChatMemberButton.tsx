import useAuthPost from "../../hooks/useAuthPost";
import add_user_icon from "../../assets/add-icon.png";

type Props = {
    chat_id: string;
};

export default function ChatMemberButton({ chat_id }: Props) {
    const { post, loading } = useAuthPost();

    const handleClick = async () => {
        const data = prompt(`Enter ID of the user to add to chat: `);
        if (data == null || data.trim() == "") {
            return;
        }
        const user_id = parseInt(data.trim());

        const payload = { chat_id, user_id };
        try {
            await post("/chat-member/join", payload);
        } catch (err) { 
            alert("Failed to add user: " + err);
        }
    };

    return (
        <div 
            className={`flex items-center gap-3 p-2 hover:bg-gray-100 rounded transition cursor-pointer ${loading ? "opacity-50 pointer-events-none" : ""}`}
            onClick={handleClick}
        >
            <img
                src={add_user_icon}
                alt={"Add User Icon"}
                className="w-12 h-12 rounded-full object-cover"
            />
            <h2 className="font-semibold text-gray-900">Add new chat member</h2>
        </div>
    );
}
