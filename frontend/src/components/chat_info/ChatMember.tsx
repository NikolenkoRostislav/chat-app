import useFetch from '../../hooks/useFetch';
import useAuthDelete from '../../hooks/useAuthDelete';
import RouteButton from '../RouteButton';
import default_pfp from '../../assets/default-pfp.png';

export type ChatMemberType = {
    refresh: () => void;
    member_id: string;
    user_id: string;
    chat_id: string;
    show_delete_button: boolean;  
};

type Props = {
    member: ChatMemberType;
};

export default function ChatMember({ member }: Props) {
    const {data: user_data, loading: user_loading, error: user_error} = useFetch(`/user/id/${member.user_id}`)
    //const {data: member_data, loading: member_loading, error: member_error} = useFetch(`/chat-member/role/${member.member_id}`)
    const {delete_func} = useAuthDelete();

    const onRemove = async (e: React.MouseEvent) => {
        e.preventDefault();

        const payload = {
            user_id: member.user_id,
            chat_id: parseInt(member.chat_id),
        };

        try {
            await delete_func(`/chat-member/remove-member`, payload);
            member.refresh();
        } catch (err) {
            alert("Failed to remove member: " + err);
        }
    }

    if (user_error /*|| member_error*/) return <p>{user_error /*|| member_error*/}</p>;
    if (user_loading /*|| member_loading*/) return (<p>Loading user data...</p>)

    return (
        <RouteButton route={`/user/${user_data.username}`}>
            <div className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded transition">
                <img
                    src={user_data.pfp_url}
                    alt={`${user_data.username}'s profile picture`}
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_pfp;
                    }}
                    className="w-12 h-12 rounded-full object-cover"
                />
                <h2 className="font-semibold text-gray-900">{user_data.username}</h2>
                {member.show_delete_button && <button 
                    onClick={onRemove} 
                    className="ml-auto w-8 h-8 rounded-full object-cover border border-gray-300 cursor-pointer hover:bg-gray-200"
                >
                    <strong>X</strong>
                </button>
                }
                {/*member_data.is_admin && <span className="text-sm text-blue-500">Admin</span>*/}
            </div>
        </RouteButton>
    );
}
