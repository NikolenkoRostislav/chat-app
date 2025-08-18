import useAuthRequest from "./useAuthRequest";

/**
* Custom hook to delete data from backend.
* @param {string} route - The API route to post data to (must start with '/').
* @param {any} payload - The data object to be sent in the request body (will be JSON.stringified).
* @returns {Object} - { delete_func, data, loading }
*   - delete_func(route: string, payload: any): Promise<T> - Function to send PATCH request.
*   - data: response data from the server or null before response.
*   - loading: boolean loading state
* @example
* const { delete_func } = useAuthDelete();
* ...
* const data = await patch("/user/update/username", payload);
*/

export default function useAuthDelete<T = any>() {
    const { func, data, loading } = useAuthRequest<T>();
    const delete_func = (route: string, payload: any) => func(route, "DELETE", payload);
    return { delete_func, data, loading };
}
