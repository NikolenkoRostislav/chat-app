import { Link } from "react-router-dom";
import type { ReactNode } from "react";

type Props = {
    route: string;
    children: ReactNode;
};

export default function RouteButton({route, children}: Props) {
    return (
        <>  
            <Link to={`/${route}`}>
                {children}
            </Link>
        </>
    );
}