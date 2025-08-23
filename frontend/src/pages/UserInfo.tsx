import { useParams } from 'react-router-dom';
import useFetch from '../hooks/useFetch';
import HomeButton from '../components/general/HomeButton';
import default_pfp from '../assets/default-pfp.png';

export default function UserInfo() {
    const { username } = useParams<{ username: string }>();

    if (!username) return <p className="text-center mt-10">No username provided.</p>;

    const { data: user, loading, error } = useFetch(`/user/${username}`);

    if (loading) return <p className="text-center mt-10">Loading user data...</p>;
    if (error) return <p>Error: {error}</p>;
    if (!user) return <p>User not found.</p>;

    const rawDate = user.last_online;
    const cleanedDateStr = rawDate.split('.')[0] + 'Z';
    const lastOnlineDate = new Date(cleanedDateStr);

    return (
        <>
            <nav className="m-4">
                <HomeButton />
            </nav>
            <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
                <h1 className="text-2xl font-bold mb-4">{user.username}'s Profile</h1>
                <img 
                    src={user.pfp_url} 
                    alt="Profile" 
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_pfp;
                    }}
                    className="w-32 h-32 rounded-full object-cover mx-auto mb-4" 
                />
                <p><strong>Username:</strong> {user.username}</p>
                <div>
                    <strong>Last online: </strong> 
                    <time dateTime={lastOnlineDate.toISOString()}>
                        {lastOnlineDate.toLocaleString(undefined, {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                            hour: "2-digit",
                            minute: "2-digit"
                        })}
                    </time>
                </div>
            </main>
        </>
    );
}
