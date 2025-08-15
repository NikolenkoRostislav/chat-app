import useRequest from "./useRequest";

/**
* Custom hook to post data to backend.
* @param {string} route - The API route to post data to (must start with '/').
* @param {any} payload - The data object to be sent in the request body (will be JSON.stringified).
* @param {boolean} [urlencoded=false] - Whether to send data as URL-encoded form data instead of JSON.
* @returns {Object} - { post, data, loading }
*   - post(route: string, payload: any): Promise<T> - Function to send POST request.
*   - data: response data from the server or null before response.
*   - loading: boolean loading state
* @example
* const { post, loading } = usePost();
* ...
* const data = await post("/user/register", payload);
*/

export default function usePost<T = any>() {
    const { func, data, loading } = useRequest<T>();
    const post = (route: string, payload: any, urlencoded = false ) => func(route, "POST", payload, urlencoded);
    return { post, data, loading };
}
