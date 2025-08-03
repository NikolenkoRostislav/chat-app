import useAuthFetch from "../hooks/useAuthFetch";

export default function UserMe() {
    const { data: user, loading, error } = useAuthFetch("/user/me");

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <main className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
            <img src={user?.pfp_url} alt="Profile" className="w-32 h-32 rounded-full mx-auto mb-4" />
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Username:</strong> {user?.username}</p>
        </main>
    );
}
