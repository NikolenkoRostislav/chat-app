import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

export default function UserInfo() {
    const { username } = useParams<{ username: string }>();
    const [user, setUser] = useState<any>(null);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_URL}/user/${username}`)
        .then(res => {
            if (!res.ok) throw new Error("user not found");
            return res.json();
        })
        .then(data => setUser(data))
        .catch(console.error);
    }, [username]);

    if (!user) return <p className="text-center mt-10">Loading user data...</p>;

    const rawDate = user.last_online;
    const cleanedDateStr = rawDate.split('.')[0] + 'Z';
    const lastOnlineDate = new Date(cleanedDateStr);

    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-4">{user.username}'s Profile</h1>
            <img src={user.pfp_url} alt="Profile" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <p><strong>Username:</strong> {user.username}</p>
            <div>
                <strong>Last online: </strong> 
                <time dateTime={lastOnlineDate.toISOString()}>
                    {lastOnlineDate.toLocaleString()}
                </time>
            </div>
        </main>
    );
}
