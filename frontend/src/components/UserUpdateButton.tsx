import type { ReactNode } from "react";
import useAuthPatch from "../hooks/useAuthPatch";

type Props = {
    route: string;
    field_name: string;
    children: ReactNode;
};

export default function UserUpdateButton({ route, field_name, children }: Props) {
    const { patch, loading } = useAuthPatch();

    const handleClick = async () => {
        const data = prompt(`Enter new value for ${field_name}:`);
        if (data == null || data.trim() == "") {
            return;
        }

        const payload = { 
            [field_name]: data,
        };
        try {
            await patch(route, payload);
        } catch (err) {
            alert(`Failed to update: ${err}`);
        }
    };

    return (
            <div 
                onClick={handleClick}
                className={`cursor-pointer hover:bg-gray-100 rounded p-2 ${loading ? "opacity-50 pointer-events-none" : ""}`}
            >
                {children}
            </div>
    );
}