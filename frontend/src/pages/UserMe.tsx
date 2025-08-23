import { useEffect, useState } from "react";
import useAuthFetch from "../hooks/useAuthFetch";
import UserUpdateButton from "../components/user_info/UserUpdateButton";
import HomeButton from "../components/general/HomeButton";
import default_pfp from '../assets/default-pfp.png';

export default function UserMe() {
    const { data: user, loading, error, refetch } = useAuthFetch("/user/me");

    const [display_username, setUsername] = useState(" ");
    const [display_pfp_url, setPfpUrl] = useState(" ");
    const [display_email, setEmail] = useState(" ");

    useEffect(() => {
        if (user) {
            setUsername(user.username);
            setPfpUrl(user.pfp_url);
            setEmail(user.email);
        }
    }, [user]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <>  
            <nav className="m-4">
                <HomeButton />
            </nav>
            <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
                <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
                
                <UserUpdateButton route="/user/update/pfp" field_name="pfp_url" refresh={refetch}>
                    <img 
                        src={display_pfp_url} 
                        alt="Profile picture" 
                        onError={(e) => {
                            const img = e.target as HTMLImageElement;
                            img.onerror = null;
                            img.src = default_pfp;
                        }}
                        className="w-32 h-32 rounded-full mx-auto mb-4" 
                    />
                </UserUpdateButton>
                <UserUpdateButton route="/user/update/email" field_name="email" refresh={refetch}>
                    <p><strong>Email:</strong> {display_email}</p>
                </UserUpdateButton>
                <UserUpdateButton route="/user/update/username" field_name="username" refresh={refetch}>
                    <p><strong>Username:</strong> {display_username}</p>
                </UserUpdateButton>
                <div className="p-2">
                    <p><strong>User ID:</strong> {user.id}</p>  
                </div>
            </main>
        </>
    );
}
