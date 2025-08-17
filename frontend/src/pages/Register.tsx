import { useState } from "react";
import { useNavigate } from "react-router-dom";
import RouteButton from "../components/RouteButton";
import usePost from "../hooks/usePost";

export default function Register() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { post, loading } = usePost();

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const payload = {
            email,
            username,
            password,
            pfp_url: " "
        };

        try {
            const data = await post("/user/register", payload);
            console.log("Registered successfully! User ID:", data.user_id);
            navigate("/login");
        } catch (err) {
            alert("Registration failed: " + err);
        }
    };

    return (
        <main>
            <div className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
                <h1 className="text-2xl font-bold mb-6 text-center">Register</h1>

                <form onSubmit={onSubmit} className="flex flex-col gap-4">
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
                            type="text"
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
                        {loading ? "Registering..." : "Register"}
                    </button>
                </form>
            </div>
            <div className="text-center mt-4">
                <RouteButton route="login">
                    <p className="text-blue-600 hover:underline">Already have an account? Login here</p>
                </RouteButton>
            </div>
        </main>
    );
}
