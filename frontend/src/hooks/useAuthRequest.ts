import { useState } from "react";
import { useNavigate } from "react-router-dom";

type Method = "POST" | "PATCH" | "PUT" | "DELETE";

export default function useAuthRequest<T = any>() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<T | null>(null);
    const navigate = useNavigate();

    const func = async (route: string, method: Method, payload: any) => {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Not logged in!");
            navigate("/login");
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {
                method: method,
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || response.statusText);
            }

            const result = await response.json();
            setData(result);
            return result;
        } catch (err: any) {
            console.error(err);
            setError(err.message || `${method} request failed`);
            setData(null);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return { func, data, loading, error };
}
