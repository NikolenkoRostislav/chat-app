import { useEffect, useState } from "react";

/**
 * Custom hook to fetch authenticated data from backend.
 * @param {string} route - The API route to fetch data from (must start with '/').
 * @returns {Object} - { data, loading, error }
 *   - data: fetched data or null while loading
 *   - loading: boolean loading state
 *   - error: error message or null
 *
 * @example
 * const { data: user, loading, error } = useFetch("/user/{username}");
 */

export default function useFetch<T = any>(route: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        setError(null);

        fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`)
        .then(res => {
            if (!res.ok) throw new Error("Fetch failed");
            return res.json();
        })
        .then(json => {setData(json);})  
        .catch(err => {
            console.error(err); 
            setError(err.message || "Failed to fetch");
        })
        .finally(() => setLoading(false));
    }, [route]);

    return { data, loading, error };
}
