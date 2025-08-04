import useAuthFetch from "../hooks/useAuthFetch";

export default function useCurrentUserID() {
    const { data: user, loading, error } = useAuthFetch("/user/me");

    return {id: user?.id, loading, error};
}
