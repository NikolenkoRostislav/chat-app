import { useState } from "react";
import useAuthPatch from "../hooks/useAuthPatch";

type Props = {
    route: string;
    field_name: string;
};

export default function UserUpdateButton({ route, field_name }: Props) {
    const { patch, loading } = useAuthPatch();
    const [data, setData] = useState("");

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();

        const payload = { 
            [field_name]: data,
        };
        try {
            await patch(route, payload);
            setData("");
        } catch (err) {
            alert(`Failed to update: ${err}`);
        }
    };

    return (
        <form onSubmit={handleSend}>
            <textarea
                value={data}
                onChange={e => setData(e.target.value)}
                required
                placeholder="..."
            />

            <button 
                type="submit" 
                disabled={loading}
            >
                Update something, this is a placeholder anyways
            </button>
        </form>
    );
}