import { useState } from "react";
import { useNavigate } from "react-router-dom";

type Method = "POST" | "PATCH" | "PUT" | "DELETE";

export default function useAuthRequest<T = any>() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<T | null>(null);
    const navigate = useNavigate();

    const func = async (route: string, method: Method, payload: any) => {
        setLoading(true);

        const token = localStorage.getItem("token");
        if (!token) {
            console.log("Token missing or expired, redirecting to login page");
            navigate("/login");
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}${route}`, {
                method: method,
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify(payload),
                credentials: "include"
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
