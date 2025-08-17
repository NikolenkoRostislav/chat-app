import add_chat_icon from '../../assets/add-icon.png';

type Props = {
    setChatCreationMenuOpen: (open: boolean) => void;
};

export default function ChatButton({ setChatCreationMenuOpen }: Props) {
    const onClick = () => {
        setChatCreationMenuOpen(true);
    }

    return (
        <div 
            className="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer"
            onClick={onClick}
        >
            <img 
                src={add_chat_icon} 
                alt="Add Chat Icon" 
                className="w-18 h-18 rounded-full object-cover border border-gray-300" 
            />
            <h2 className="text-lg font-semibold truncate">Create New Chat</h2>
        </div>
    );
}