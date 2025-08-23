import { useState } from "react";
import { useNavigate } from "react-router-dom";
import usePost from "../hooks/usePost";
import RouteButton from "../components/general/RouteButton";
import { socket } from "../socket";

export default function Login() {
    const { loading, post } = usePost();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const socket_connect = async (token: string) => {
        if (!socket.connected) {
            await new Promise<void>((resolve) => {
                socket.once("connect", () => resolve());
                socket.connect();
            });
        }

        socket.emit("identify_user", {token})
    }

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const payload = { username, password };

        try {
            const result = await post(`/user/auth/login`, payload, true);
            localStorage.setItem("token", result.access_token);
            await socket_connect(result.access_token);
            navigate("/");
        } catch (err) { 
            alert("Login failed: " + err);
        } 
    };

    return (
        <main>
            <div className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
                <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>

                <form onSubmit={onSubmit} className="flex flex-col gap-4">
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
                        {loading ? "Logging in..." : "Log In"}
                    </button>
                </form>
            </div>
            <div className="text-center mt-4">
                <RouteButton route="/register">
                    <p className="text-blue-600 hover:underline">Don't have an account? Register here</p>
                </RouteButton>
            </div>
        </main>
        
    );
}
