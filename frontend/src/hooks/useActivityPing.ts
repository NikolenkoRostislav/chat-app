import { useEffect } from "react";
import useAuthPatch from "./useAuthPatch";

export default function useActivityPing(){
    const {patch: ping} = useAuthPatch();

    useEffect(() => {
        setInterval(async () => {
            try {
                await ping("/user/update/last-online", {});
            } catch (err) {
                console.log(err);
            }
        }, 60 * 1000 );
    }, []);

    return null;
}