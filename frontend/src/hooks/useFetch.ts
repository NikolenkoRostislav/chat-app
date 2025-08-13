import { useEffect, useState } from "react";

/**
 * Custom hook to fetch data from backend.
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

    const fetch_data = async (route: string) => {
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
    }

    useEffect(() => {
        fetch_data(route);
    }, [route]);

    return { data, loading, error };
}
