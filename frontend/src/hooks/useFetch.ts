import { useEffect, useState, useCallback } from "react";

/**
* Custom hook to fetch data from backend.
* @param {string} route - The API route to fetch data from (must start with '/').
* @returns {Object} - { data, loading, error, refetch }
*   - data: fetched data or null while loading
*   - loading: boolean loading state
*   - error: error message or null
*   - refetch: function to refetch data
*
* @example
* const { data: user, loading, error } = useFetch("/user/{username}");
*/

export default function useFetch<T = any>(route: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const fetch_data = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`);

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || response.statusText);
            }

            setData(data);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Failed to fetch");
        } finally {
            setLoading(false);
        }
    }, [route]);

    useEffect(() => {
        fetch_data();
    }, [fetch_data]);

    return { data, loading, error, refetch: fetch_data };
}
