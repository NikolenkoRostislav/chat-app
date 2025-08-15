import useAuthRequest from "./useAuthRequest";

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

export default function useAuthPost<T = any>() {
    const { func, data, loading } = useAuthRequest<T>();
    const post = (route: string, payload: any) => func(route, "POST", payload);
    return { post, data, loading };
}
