import {io, Socket} from "socket.io-client"

export const socket: Socket = io(import.meta.env.VITE_BACKEND_URL, { 
    autoConnect: false, 
    path: "/ws/socket.io",
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
});

socket.on("connect", () => {
    console.log("connected");
    const token = localStorage.getItem("token");
    socket.emit("identify_user", {token})
})
        
socket.on("disconnect", () => {
    console.log("disconnected")
})