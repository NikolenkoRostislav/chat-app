import RouteButton from "./RouteButton";
import default_pfp from '../assets/default-pfp.png';
import useAuthFetch from "../hooks/useAuthFetch";

export default function UserInfoButton() {
    const { data: user, loading } = useAuthFetch("/user/me");

    if (loading || !user) return (
        <img
            src={default_pfp}
            alt={"User Info Loading"}
            className="w-15 h-15 rounded-full object-cover"
        />
    );

    return (
        <RouteButton route="/user/me">
            <div className="flex items-center space-x-2">
                <img
                    src={user.pfp_url}
                    alt={"User Info"}
                    onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.onerror = null;
                        img.src = default_pfp;
                    }}
                    className="w-15 h-15 rounded-full object-cover"
                />
                <span className="font-semibold">{user.username}</span>
            </div>
        </RouteButton>  
    );
}