import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await fetch(`${BACKEND_URL}/user/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: formData.toString(),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert("Login failed: " + (errorData.detail || response.statusText));
                return;
            }

            const data = await response.json();
            console.log("Logged in! Token:", data.access_token);
            localStorage.setItem("token", data.access_token);
            navigate("/");
        } catch (err) {
            alert("Network error, please try again later.");
            console.error(err);
        }
    };

    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
                    Log In
                </button>
            </form>
        </main>
    );
}
