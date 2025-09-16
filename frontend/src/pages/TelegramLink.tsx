import { useState, useEffect } from "react";
import HomeButton from "../components/general/HomeButton";
import useAuthPost from "../hooks/useAuthPost";

export default function TelegramLink() {
    const { post, loading } = useAuthPost();
    const [code, setCode] = useState("");

    useEffect(() => {
        const fetchCode = async () => {
            const result = await post('/tg-connection/temp-code', {});
            setCode(result.code);
        };
        fetchCode();
    }, []);

    return (
        <>  
            <nav className="m-4">
                <HomeButton />
            </nav>
            <main className="max-w-md mx-auto mt-24 p-8 border rounded-2xl shadow-lg bg-white">
                <h1 className="text-xl font-bold mb-2 text-center">
                    Use this code to link your account with 
                </h1>
                <h1 className="text-2xl font-bold mb-4 text-center">
                    <a href={import.meta.env.VITE_TELEGRAM_BOT_URL} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        OUR TELEGRAM BOT
                    </a>
                </h1>
                <div className="text-center text-4xl font-mono p-6 border-2 border-dashed rounded-2xl bg-gray-50 select-all">
                    {loading ? "loading" : code}
                </div>
                <p className="mt-6 text-center text-gray-600">
                    After linking your account, you can use our bot to receive notifications about new messages.
                </p>
            </main>
        </>
    );
}
