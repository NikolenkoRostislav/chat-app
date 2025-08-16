import { useState } from "react";

type Method = "POST" | "PATCH" | "PUT" | "DELETE";

export default function useAuthRequest<T = any>() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<T | null>(null);

    const func = async (route: string, method: Method, payload: any, urlencoded = false) => {
        setLoading(true);

        try {
            let body;
            if (urlencoded) {
                const formData = new URLSearchParams();
                for (const key in payload) {
                    formData.append(key, payload[key]);
                }
                body = formData.toString();
            } else {
                body = JSON.stringify(payload);
            }

            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {
                method: method,
                headers: { "Content-Type": urlencoded ? "application/x-www-form-urlencoded" : "application/json"},
                body: body
            });

            const result = await response.json();
            if (!response.ok) {
                let error_msg = "Request failed";

                if (result.detail) {
                    if (Array.isArray(result.detail)) {
                        error_msg = result.detail[0].msg;
                    } else {
                        error_msg = result.detail;
                    }
                } else if (result.message) {
                    error_msg = result.message;
                }

                throw new Error(error_msg);
            }
            setData(result);
            return result;
        } catch (err: any) {
            console.error(err);
            setData(null);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return { func, data, loading };
}
