import { useEffect } from "react";
import useAuthDelete from "../../hooks/useAuthDelete";
import { socket } from "../../socket";

type Props = {
    setDeletePos: any;
    chat_id: number;
    id: number;
    x: number;
    y: number;
};

export default function DeleteMessageButton({ id, chat_id, x, y, setDeletePos }: Props) {
    const {delete_func} = useAuthDelete()

    useEffect(() => {
        const handleGlobalClick = () => setDeletePos(null);
        document.addEventListener("click", handleGlobalClick);

        return () => {
            document.removeEventListener("click", handleGlobalClick);
        };
    }, []);

    const onDelete = async () => {
        await delete_func(`/message/${id}`, {})
        socket.emit("new_message_sent", {chat_id: chat_id})
    }

    return (
        <div 
            className="absolute bg-gray-700 text-white px-2 py-1 rounded z-50 cursor-pointer" 
            style={{ top: y, left: x }}
            onClick={() => onDelete()}
        >
            Delete Message
        </div>
    );
}
