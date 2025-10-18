FastAPI WebSocket Chat

A simple real-time chat application using FastAPI and WebSockets. Users can join topic-based rooms, chat in real-time, and list active topics.

Features

Real-time messaging in topic rooms

Unique usernames per topic (suffix # if duplicate)

Messages include username, message, and timestamp

Messages expire after 30 seconds

/list shows active topics and user counts

Empty topics are removed automatically

Setup
1. Clone the Repository
git clone https://github.com/albertthomas2205/chatapp.git
cd chatapp

2. Create Virtual Environment
python -m venv venv

3. Activate Virtual Environment

Windows (cmd):

venv\Scripts\activate


Windows (PowerShell):

venv\Scripts\Activate.ps1


Linux / macOS:

source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt


If requirements.txt does not exist, run:

pip install fastapi uvicorn websockets
pip freeze > requirements.txt

Run the Server
uvicorn main:app --reload


Server WebSocket endpoint: ws://localhost:8000/ws

Run the Client
python client_example.py


Enter username and topic to join

Type messages to chat

/list → Show active topics and user counts

c → Quit

Example Session
Enter username: alice
Enter topic: sports
[Info] Welcome alice to sports!
Hello everyone!
[2025-10-18 16:22:31] bob: Hi Alice!
/list
Active topics:
  sports: 2 user(s)

Notes

Fully in-memory; no database required

Multiple clients can connect to the same or different topics

Messages are automatically removed after 30 seconds
