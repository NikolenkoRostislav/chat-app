import useAuthRequest from "./useAuthRequest";

/**
 * Custom hook to patch data to backend.
 * @param {string} route - The API route to post data to (must start with '/').
 * @param {any} payload - The data object to be sent in the request body (will be JSON.stringified).
 * @returns {Object} - { patch, data, loading, error }
 *   - patch(route: string, payload: any): Promise<T> - Function to send PATCH request.
 *   - data: response data from the server or null before response.
 *   - loading: boolean loading state
 *   - error: error message or null
 * @example
* const { patch, loading, error } = usePost();
* ...
* const data = await patch("/user/update/username", payload);
*/

export default function useAuthPatch<T = any>() {
    const { func, data, loading, error } = useAuthRequest<T>();
    const patch = (route: string, payload: any) => func(route, "PATCH", payload);
    return { patch, data, loading, error };
}
