import { useState } from "react";

/**
 * Custom hook to post data to backend.
 * @param {string} route - The API route to post data to (must start with '/').
 * @param {any} payload - The data object to be sent in the request body (will be JSON.stringified).
 * @returns {Object} - { post, data, loading, error }
 *   - post(route: string, payload: any): Promise<T> - Function to send POST request.
 *   - data: response data from the server or null before response.
 *   - loading: boolean loading state
 *   - error: error message or null
 * @example
* const { post, loading, error } = usePost();
* ...
* const data = await post("/user/register", payload);
*/

export default function usePost<T = any>() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<T | null>(null);

    const post = async (route: string, payload: any) => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
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
            setError(err.message || "Post failed");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return { post, data, loading, error };
}
