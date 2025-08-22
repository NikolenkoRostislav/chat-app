import RouteButton from "../RouteButton";

const onClick = () => {
    localStorage.removeItem("token");
}

export default function HomeButton() {
    return (
        <RouteButton route="/login">
            <p className="text-red-500" onClick={onClick}><strong>Logout</strong></p>
        </RouteButton>
    );
}