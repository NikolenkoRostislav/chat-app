import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * Custom hook to fetch authenticated data from backend.
 * @param {string} route - The API route to fetch data from (must start with '/').
 * @returns {Object} - { data, loading, error }
 *   - data: fetched data or null while loading
 *   - loading: boolean loading state
 *   - error: error message or null
 *
 * @example
 * const { data: user, loading, error } = useAuthFetch("/user/me");
 */

export default function useAuthFetch<T = any>(route: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Not logged in!");
            navigate("/login");
            return;
        }

        setLoading(true);
        setError(null);

        fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {
            headers: {
                "Authorization": `Bearer ${token}`,
            }
        })
        .then(res => {
            if (!res.ok) throw new Error("Unauthorized");
            return res.json();
        })
        .then(json => {
            setData(json);
        })
        .catch(err => {
            console.error(err);
            setError(err.message || "Failed to fetch");
            alert("Session expired. Please login again.");
            navigate("/login");
        })
        .finally(() => setLoading(false));
    }, [navigate, route]);

    return { data, loading, error };
}
