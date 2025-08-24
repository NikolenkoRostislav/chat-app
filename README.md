<h1 align="center">
  <img src="assets/Chat_App_Banner.png" alt="Chat App Banner" width="800"/>
  <br>
  Chat App
</h1>

<h4 align="center">
    A fullstack real-time chat web app built with 
    <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> + 
    <a href="https://www.typescriptlang.org/" target="_blank">TypeScript</a> + 
    <a href="https://react.dev/" target="_blank">React</a> + 
    <a href="https://socket.io/" target="_blank">Socket.IO</a>.
</h4>

<p align="center">
    <a href="#introduction">Intro</a> •
    <a href="#features">Features</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#setup">Setup</a> •
    <a href="#contact">Contact</a>
</p>

---

## Introduction

Chat App is a simple messaging web app built with **FastAPI + SQLAlchemy + Socket.IO** (backend) and **React + TypeScript** (frontend).  
It allows users to create accounts, join chats, and send messages in a clean and user-friendly interface.

This project was built as part of my learning process for fullstack development, focusing on authentication,  
database relations, frontend–backend communication and live sockets.  

Future versions may include features like dark theme and improved chatroom management.

---

## Features

- JWT-based authentication
- Session management with secure refresh tokens stored in HTTP-only cookies
- Real-time messaging with Socket.IO
- Create, join, delete and view chats
- Add and remove chat members
- View user profiles
- Update your profile

---

## Tech Stack

**Frontend:**

- Vite + React
- TypeScript
- React Router DOM

**Backend:**

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Socket.IO

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NikolenkoRostislav/chat-app.git
cd chat-app
```

### 2. Environment variables

Create a `.env` file in the `backend` folder with the following variables:
```env
DATABASE_URL=sqlite+aiosqlite:///./your_database_name.db
SECRET_KEY=your_jwt_secret_here
ALGORITHM=HS256
```
Create a second `.env` file in the `frontend` folder
```env
VITE_BACKEND_URL=http://localhost:8000
```

### 3. Backend setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:socket_app --reload
```

### 4. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### 5. Open in browser

Go to `http://localhost:5173` to see the app running!

---

## Contact

You can contact me via:  
Work Email: rostislavnikolenkowork@gmail.com  
Personal Email: rostislav160307@gmail.com  
LinkedIn: [linkedin.com/in/rostyslav-nikolenko-58b069348](https://www.linkedin.com/in/rostyslav-nikolenko-58b069348)  
Telegram: @RSlavNV  