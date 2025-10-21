
import json
import asyncio
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

app = FastAPI()

# Store users per topic: topic -> {username: websocket}
topic_users: Dict[str, Dict[str, WebSocket]] = {}

# Store messages per topic: topic -> list of (message_dict, timestamp)
topic_messages: Dict[str, List[tuple]] = {}

# Message expiry task
async def expire_messages(topic: str):
    while True:
        await asyncio.sleep(5)
        now = time.time()
        # If topic no longer exists, stop task
        if topic not in topic_messages:
            break
        # Remove expired messages
        topic_messages[topic] = [
            (m, ts) for m, ts in topic_messages[topic] if now - ts < 30
        ]
        # Stop task if no users left
        if topic not in topic_users or not topic_users[topic]:
            topic_messages.pop(topic, None)
            break

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = None
    topic = None
    try:
        payload = await websocket.receive_text()
        try:
            payload_json = json.loads(payload)
        except json.JSONDecodeError:
            await websocket.send_json({"error": "Invalid JSON payload."})
            await websocket.close(code=4001)
            return

        username = payload_json.get("username")
        topic = payload_json.get("topic")
        if not username or not topic or not isinstance(username, str) or not isinstance(topic, str):
            await websocket.send_json({"error": "Username and topic (as strings) required."})
            await websocket.close(code=4001)
            return

        # Ensure unique username in topic
        users = topic_users.setdefault(topic, {})
        orig_username = username
        suffix = 1
        while username in users:
            username = f"{orig_username}#{suffix}"
            suffix += 1
        users[username] = websocket

        # Start message expiry task if not exists
        if topic not in topic_messages:
            topic_messages[topic] = []
            asyncio.create_task(expire_messages(topic))

        await websocket.send_json({"info": f"Welcome {username} to {topic}!"})
        print(f"{username} joined {topic}")

        # Main loop to receive messages
        while True:
            try:
                data_text = await websocket.receive_text()
                try:
                    data = json.loads(data_text)
                except json.JSONDecodeError:
                    await websocket.send_json({"error": "Invalid JSON message."})
                    continue

                msg = data.get("msg")
                if not isinstance(msg, str):
                    await websocket.send_json({"error": "Message must be a string."})
                    continue

                # Handle /list command
                if msg.strip() == "/list":
                    info = {t: f"{len(u)} user(s)" for t, u in topic_users.items()}
                    await websocket.send_json({"topics": info})
                    continue

                if msg.strip():
                    # Prepare message with timestamp
                    msg_data = {
                        "username": username,
                        "message": msg,
                        "timestamp": int(time.time())
                    }
                    ts = time.time()
                    topic_messages[topic].append((msg_data, ts))

                    # Broadcast to all users except sender
                    disconnected = []
                    for user, ws in users.items():
                        if user != username:
                            try:
                                await ws.send_json({"msg": msg_data})
                            except Exception:
                                disconnected.append(user)
                    # Remove disconnected users
                    for user in disconnected:
                        users.pop(user, None)

                    # Send ack to sender
                    await websocket.send_json({"info": "Message delivered", "msg": msg_data})

            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        print(f"{username} disconnected from {topic}")

    finally:
        # Cleanup user from topic
        if topic and username and topic in topic_users:
            topic_users[topic].pop(username, None)
            if not topic_users[topic]:
                topic_users.pop(topic, None)
                topic_messages.pop(topic, None)
