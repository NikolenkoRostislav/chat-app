import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const payload = {
            email,
            username,
            password,
            pfp_url: " "
        };

        try {
            const response = await fetch(`${BACKEND_URL}/user/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert("Registration failed: " + (errorData.detail || response.statusText));
                return;
            }

            const data = await response.json();
            console.log("Registered successfully! User ID:", data.user_id);
            navigate("/login");
        } catch (err) {
            alert("Network error, please try again later.");
            console.error(err);
        }
    };


    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-6 text-center">Register</h1>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <label>
                    Email:
                    <input
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                        className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
                        placeholder="you@example.com"
                    />
                </label>

                <label>
                    Username:
                    <input
                        type="username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        required
                        className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
                        placeholder="username"
                    />
                </label>

                <label>
                    Password:
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                        className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
                        placeholder="********"
                    />
                </label>

                <button type="submit" className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
                    Register
                </button>
            </form>
        </main>
    );
}
