import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

/**
* Custom hook to fetch authenticated data from backend.
* @param {string} route - The API route to fetch data from (must start with '/').
* @returns {Object} - { data, loading, error, refetch }
*   - data: fetched data or null while loading
*   - loading: boolean loading state
*   - error: error message or null
*   - refetch: function to refetch data
*
* @example
* const { data: user, loading, error } = useAuthFetch("/user/me");
*/

export default function useAuthFetch<T = any>(route: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const fetch_data = useCallback(async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Not logged in!");
            navigate("/login");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {headers: { "Authorization": `Bearer ${token}` }});

            const data = await response.json();
            if (!response.ok) {
                if (response.status === 401) {
                    alert("Session expired. Please login again.");
                    navigate("/login");
                    return;
                }
                throw new Error(data.detail || response.statusText);
            }

            setData(data);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Failed to fetch");
        } finally {
            setLoading(false);
        }
    }, [route, navigate]);

    useEffect(() => {
        fetch_data();
    }, [fetch_data]);

    return { data, loading, error, refetch: fetch_data };
}
