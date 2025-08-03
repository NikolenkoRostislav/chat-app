import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UserMe() {
    const [user, setUser] = useState<any>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Not logged in!");
            navigate("/login");
            return;
        }

        fetch(`${import.meta.env.VITE_BACKEND_URL}/user/me`, {
            headers: {
                "Authorization": `Bearer ${token}`,
            }
        })
        .then(res => {
            if (!res.ok) throw new Error("Unauthorized");
            return res.json();
        })
        .then(data => setUser(data))
        .catch(err => {
            console.error(err);
            alert("Session expired. Please login again.");
            navigate("/login");
        });
    }, [navigate]);

    if (!user) return <p className="text-center mt-10">Loading user data...</p>;

    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
            <img src={user.pfp_url} alt="Profile" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Username:</strong> {user.username}</p>
        </main>
    );
}
