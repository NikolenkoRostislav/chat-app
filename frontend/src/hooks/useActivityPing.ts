import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import useAuthPatch from "./useAuthPatch";

export default function useActivityPing() {
    const location = useLocation();
    const { patch: ping } = useAuthPatch();

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                if (location.pathname !== "/login" && location.pathname !== "/register") {
                    await ping("/user/update/last-online", {});
                }
            } catch (err) {
                console.log(err);
            }
        }, 60 * 1000 );

        return () => clearInterval(interval);
    }, [location.pathname, ping]);

    return null;
}