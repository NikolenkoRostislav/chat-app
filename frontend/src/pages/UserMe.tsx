import useAuthFetch from "../hooks/useAuthFetch";
import UserUpdateButton from "../components/UserUpdateButton";
import default_pfp from '../assets/default-pfp.png';

export default function UserMe() {
    const { data: user, loading, error } = useAuthFetch("/user/me");

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
            <img 
                src={user?.pfp_url} 
                alt="Profile" 
                onError={(e) => {
                    const img = e.target as HTMLImageElement;
                    img.onerror = null;
                    img.src = default_pfp;
                }}
                className="w-32 h-32 rounded-full mx-auto mb-4" 
            />
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Username:</strong> {user?.username}</p>
            {/*<UserUpdateButton route="/user/update/pfp" field_name="new_pfp" />*/}
        </main>
    );
}
