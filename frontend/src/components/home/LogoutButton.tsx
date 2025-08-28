import usePost from "../../hooks/usePost";
import RouteButton from "../general/RouteButton";

export default function HomeButton() {
    const {post} = usePost(); 

    const onClick = () => {
        localStorage.removeItem("token");
        post("/auth/logout", {});
    }

    return (
        <RouteButton route="/login">
            <p className="text-red-500" onClick={onClick}><strong>Logout</strong></p>
        </RouteButton>
    );
}