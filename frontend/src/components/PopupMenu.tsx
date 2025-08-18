import type { ReactNode } from "react";

type Props = {
    setMenuOpen: (open: boolean) => void;
    children: ReactNode;
};

export default function PopupMenu({setMenuOpen, children}: Props) {
    const onClose = () => {
        setMenuOpen(false);
    }

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
            <div className="bg-white w-3/5 max-w-2xl h-2.5/5 p-6 rounded-2xl shadow-lg">
                <div className="flex justify-end">
                    <button onClick={onClose} className="w-10 h-10 rounded-full object-cover border border-gray-300 cursor-pointer hover:bg-gray-100">
                        <strong>X</strong>
                    </button>
                </div>
                <div className="mt-4">
                    {children}
                </div> 
            </div>
        </div>
    );
}