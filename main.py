# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# from typing import Dict

# app = FastAPI()

# # {topic: {username: websocket}}
# topic_users: Dict[str, Dict[str, WebSocket]] = {}
# # {topic: [(msg, timestamp)]}
# topic_messages: Dict[str, list] = {}

# async def expire_messages(topic: str):
#     while True:
#         await asyncio.sleep(5)
#         if topic in topic_messages:
#             now = asyncio.get_event_loop().time()
#             topic_messages[topic] = [
#                 (msg, ts) for msg, ts in topic_messages[topic]
#                 if now - ts < 60
#             ]

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         payload = await websocket.receive_json()
#         username = payload.get("username")
#         topic = payload.get("topic")
#         if not username or not topic:
#             await websocket.send_json({"error": "Username and topic required."})
#             await websocket.close(code=4001)
#             return

#         # Ensure unique username in topic
#         users = topic_users.setdefault(topic, {})
#         suffix = 1
#         orig_username = username
#         while username in users:
#             username = f"{orig_username}_{suffix}"
#             suffix += 1

#         users[username] = websocket

#         # Spawn message expiration for this topic if not active
#         if topic not in topic_messages:
#             topic_messages[topic] = []
#             asyncio.create_task(expire_messages(topic))

#         await websocket.send_json({"info": f"Welcome {username} to {topic}!"})

#         while True:
#             try:
#                 data = await websocket.receive_json()
#             except Exception as ex:
#                 # Unexpected data or disconnect
#                 print("Error receiving message:", ex)
#                 break

#             print(f"Received from {username} in {topic}: {data}")
#             msg = data.get("msg")
#             if msg == "/list":
#                 info = {
#                     topic: list(topic_users[topic].keys())
#                     for topic in topic_users
#                 }
#                 await websocket.send_json({"topics": info})
#                 continue

#             if msg:
#                 ts = asyncio.get_event_loop().time()
#                 topic_messages[topic].append((f"{username}: {msg}", ts))

#                 for user, ws in users.items():
#                     if user != username:
#                         try:
#                             await ws.send_json({"msg": f"{username}: {msg}"})
#                         except Exception as ex:
#                             print(f"Failed to send to {user}: {ex}")
#                 await websocket.send_json({"info": "Message delivered"})

#     except WebSocketDisconnect:
#         print(f"{username} disconnected from topic {topic}")
#         # Remove user on disconnect
#         if topic in topic_users:
#             topic_users[topic].pop(username, None)
#             if not topic_users[topic]:
#                 topic_users.pop(topic)
#                 topic_messages.pop(topic)
#     except Exception as e:
#         print(f"General error: {e}")
#         try:
#             await websocket.send_json({"error": str(e)})
#             await websocket.close(code=4000)
#         except:
#             pass


# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# from typing import Dict

# app = FastAPI()

# topic_users: Dict[str, Dict[str, WebSocket]] = {}
# topic_messages: Dict[str, list] = {}

# async def expire_messages(topic: str):
#     while topic in topic_messages:
#         await asyncio.sleep(5)
#         now = asyncio.get_event_loop().time()
#         topic_messages[topic] = [
#             (msg, ts) for msg, ts in topic_messages[topic]
#             if now - ts < 120
#         ]

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     username = None
#     topic = None
#     try:
#         payload = await websocket.receive_json()
#         username = payload.get("username")
#         topic = payload.get("topic")
#         if not username or not topic or not isinstance(username, str) or not isinstance(topic, str):
#             await websocket.send_json({"error": "Username and topic (as strings) required."})
#             await websocket.close(code=4001)
#             return

#         users = topic_users.setdefault(topic, {})
#         orig_username = username
#         suffix = 1
#         while username in users:
#             username = f"{orig_username}_{suffix}"
#             suffix += 1
#         users[username] = websocket

#         if topic not in topic_messages:
#             topic_messages[topic] = []
#             asyncio.create_task(expire_messages(topic))
#         await websocket.send_json({"info": f"Welcome {username} to {topic}!"})

#         while True:
#             try:
#                 data = await websocket.receive_json()
#             except Exception as ex:
#                 print(f"Error receiving: {ex}")
#                 break

#             msg = data.get("msg")
#             if not isinstance(msg, str):
#                 await websocket.send_json({"error": "Message must be a string."})
#                 continue

#             if msg == "/list":
#                 info = {
#                     topic: len(users)
#                     for topic, users in topic_users.items()
#                 }
#                 await websocket.send_json({"topics": info})
#                 continue

#             if msg:
#                 ts = asyncio.get_event_loop().time()
#                 topic_messages[topic].append((f"{username}: {msg}", ts))
#                 for user, ws in users.items():
#                     if user != username:
#                         try:
#                             await ws.send_json({"msg": f"{username}: {msg}"})
#                         except Exception as ex:
#                             print(f"Failed to send to {user}: {ex}")
#                 await websocket.send_json({"info": "Message delivered"})

#     except WebSocketDisconnect:
#         print(f"{username} disconnected from {topic}")
#         if topic in topic_users:
#             topic_users[topic].pop(username, None)
#             if not topic_users[topic]:
#                 topic_users.pop(topic)
#                 topic_messages.pop(topic)
#     except Exception as e:
#         print(f"General error: {e}")
#         try:
#             await websocket.send_json({"error": str(e)})
#             await websocket.close(code=4000)
#         except:
#             pass


# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# from typing import Dict

# app = FastAPI()

# topic_users: Dict[str, Dict[str, WebSocket]] = {}
# topic_messages: Dict[str, list] = {}

# async def expire_messages(topic: str):
#     while topic in topic_messages:
#         await asyncio.sleep(5)
#         now = asyncio.get_event_loop().time()
#         topic_messages[topic] = [
#             (msg, ts) for msg, ts in topic_messages[topic]
#             if now - ts < 30
#         ]

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     username = None
#     topic = None
#     try:
#         # Handle initial connection payload
#         payload = await websocket.receive_json()
#         username = payload.get("username")
#         topic = payload.get("topic")
        
#         # Invalid payload handling
#         if not username or not topic or not isinstance(username, str) or not isinstance(topic, str):
#             await websocket.send_json({"error": "Username and topic (as strings) required."})
#             await websocket.close(code=4001)
#             return

#         # Ensure unique username in topic
#         users = topic_users.setdefault(topic, {})
#         orig_username = username
#         suffix = 1
#         while username in users:
#             username = f"{orig_username}_{suffix}"
#             suffix += 1
#         users[username] = websocket

#         # Start message expiration for new topics
#         if topic not in topic_messages:
#             topic_messages[topic] = []
#             asyncio.create_task(expire_messages(topic))

#         await websocket.send_json({"info": f"Welcome {username} to {topic}!"})

#         # Main message loop
#         while True:
#             try:
#                 data = await websocket.receive_json()
#             except Exception as ex:
#                 print(f"Error receiving: {ex}")
#                 break

#             msg = data.get("msg")
#             if not isinstance(msg, str):
#                 await websocket.send_json({"error": "Message must be a string."})
#                 continue

#             # /list command: show active topics and user counts
#             if msg == "/list":
#                 info = {
#                     topic_name: len(users_dict)
#                     for topic_name, users_dict in topic_users.items()
#                 }
#                 await websocket.send_json({"topics": info})
#                 continue

#             # Regular message handling
#             if msg:
#                 # Store message with timestamp for expiry
#                 ts = asyncio.get_event_loop().time()
#                 topic_messages[topic].append((f"{username}: {msg}", ts))
                
#                 # Broadcast to all other users in the same topic (real-time exchange)
#                 for user, ws in users.items():
#                     if user != username:
#                         try:
#                             await ws.send_json({"msg": f"{username}: {msg}"})
#                         except Exception as ex:
#                             print(f"Failed to send to {user}: {ex}")
                
#                 await websocket.send_json({"info": "Message delivered"})

#     except WebSocketDisconnect:
#         print(f"{username} disconnected from {topic}")
#         # Clean up user and topic when users leave
#         if topic in topic_users:
#             topic_users[topic].pop(username, None)
#             # Topic disappears when all users leave
#             if not topic_users[topic]:
#                 topic_users.pop(topic)
#                 topic_messages.pop(topic)
#     except Exception as e:
#         print(f"General error: {e}")
#         try:
#             await websocket.send_json({"error": str(e)})
#             await websocket.close(code=4000)
#         except:
#             pass

# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# from typing import Dict

# app = FastAPI()

# topic_users: Dict[str, Dict[str, WebSocket]] = {}
# topic_messages: Dict[str, list] = {}

# async def expire_messages(topic: str):
#     while topic in topic_messages:
#         await asyncio.sleep(5)
#         now = asyncio.get_event_loop().time()
#         topic_messages[topic] = [
#             (msg, ts) for msg, ts in topic_messages[topic]
#             if now - ts < 30
#         ]

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     username = None
#     topic = None
#     try:
#         payload = await websocket.receive_json()
#         username = payload.get("username")
#         topic = payload.get("topic")
#         if not username or not topic or not isinstance(username, str) or not isinstance(topic, str):
#             await websocket.send_json({"error": "Username and topic (as strings) required."})
#             await websocket.close(code=4001)
#             return

#         users = topic_users.setdefault(topic, {})
#         orig_username = username
#         suffix = 1
#         while username in users:
#             username = f"{orig_username}_{suffix}"
#             suffix += 1
#         users[username] = websocket

#         if topic not in topic_messages:
#             topic_messages[topic] = []
#             asyncio.create_task(expire_messages(topic))

#         await websocket.send_json({"info": f"Welcome {username} to {topic}!"})

#         while True:
#             try:
#                 data = await websocket.receive_json()
#             except Exception as ex:
#                 print(f"Error receiving: {ex}")
#                 break

#             msg = data.get("msg")
#             if not isinstance(msg, str):
#                 await websocket.send_json({"error": "Message must be a string."})
#                 continue

#             if msg == "/list":
#                 info = {t: len(u) for t, u in topic_users.items()}
#                 await websocket.send_json({"topics": info})
#                 continue

#             if msg:
#                 ts = asyncio.get_event_loop().time()
#                 topic_messages[topic].append((f"{username}: {msg}", ts))
#                 for user, ws in users.items():
#                     if user != username:
#                         try:
#                             await ws.send_json({"msg": f"{username}: {msg}"})
#                         except Exception as ex:
#                             print(f"Failed to send to {user}: {ex}")
#                 await websocket.send_json({"info": "Message delivered"})

#     except WebSocketDisconnect:
#         print(f"{username} disconnected from {topic}")
#         if topic in topic_users:
#             topic_users[topic].pop(username, None)
#             if not topic_users[topic]:
#                 topic_users.pop(topic)
#                 topic_messages.pop(topic)
#     except Exception as e:
#         print(f"General error: {e}")
#         try:
#             await websocket.send_json({"error": str(e)})
#             await websocket.close(code=4000)
#         except:
#             pass


import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

app = FastAPI()

topic_users: Dict[str, Dict[str, WebSocket]] = {}
topic_messages: Dict[str, List[tuple]] = {}


# async def expire_messages(topic: str):
#     """Automatically remove messages older than 30 seconds"""
#     while topic in topic_messages:
#         await asyncio.sleep(5)
#         now = asyncio.get_event_loop().time()
#         topic_messages[topic] = [
#             (m, ts) for m, ts in topic_messages[topic] if now - ts < 30
#         ]
#         # if no users left, clean up topic
#         if topic not in topic_users or not topic_users[topic]:
#             topic_messages.pop(topic, None)
#             break

# async def expire_messages(topic: str):
#     """Automatically remove messages older than 30 seconds"""
#     while True:
#         await asyncio.sleep(5)
#         now = asyncio.get_event_loop().time()
#         # Check if topic still exists
#         if topic not in topic_messages:
#             break
#         # Remove expired messages
#         topic_messages[topic] = [
#             (m, ts) for m, ts in topic_messages[topic] if now - ts < 30
#         ]
#         # If no users left, clean up topic messages
#         if topic not in topic_users or not topic_users[topic]:
#             topic_messages.pop(topic, None)
#             break



# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     username = None
#     topic = None
#     try:
#         # Step 1: Receive join payload
#         payload = await websocket.receive_json()
#         username = payload.get("username")
#         topic = payload.get("topic")

#         if not username or not topic or not isinstance(username, str) or not isinstance(topic, str):
#             await websocket.send_json({"error": "Username and topic (as strings) required."})
#             await websocket.close(code=4001)
#             return

#         # Step 2: Ensure unique username per topic
#         users = topic_users.setdefault(topic, {})
#         orig_username = username
#         suffix = 1
#         while username in users:
#             username = f"{orig_username}_{suffix}"
#             suffix += 1
#         users[username] = websocket

#         # Step 3: Start message expiry if not already running
#         if topic not in topic_messages:
#             topic_messages[topic] = []
#             asyncio.create_task(expire_messages(topic))

#         await websocket.send_json({"info": f"Welcome {username} to {topic}!"})
#         print(f"{username} joined {topic}")

#         # Step 4: Receive messages in real-time
#         while True:
#             data = await websocket.receive_json()
#             msg = data.get("msg")

#             if not isinstance(msg, str):
#                 await websocket.send_json({"error": "Message must be a string."})
#                 continue

#             # Handle /list command
#             # if msg.strip() == "/list":
#             #     info = {t: len(u) for t, u in topic_users.items()}
#             #     await websocket.send_json({"topics": info})
#             #     continue
            
#             if msg.strip() == "/list":
#                 # send topic info with usernames
#                 info = {
#                     t: {
#                         "count": len(u),
#                         "users": list(u.keys())
#                     }
#                     for t, u in topic_users.items()
#                 }
#                 await websocket.send_json({"topics": info})
#                 continue

#             # Normal message
#             if msg:
#                 ts = asyncio.get_event_loop().time()
#                 topic_messages[topic].append((f"{username}: {msg}", ts))

#                 # Broadcast immediately to everyone (including sender)
#                 disconnected = []
#                 for user, ws in users.items():
#                     try:
#                         await ws.send_json({"msg": f"{username}: {msg}"})
#                     except Exception:
#                         disconnected.append(user)

#                 # Remove disconnected users
#                 for user in disconnected:
#                     users.pop(user, None)

#     except WebSocketDisconnect:
#         print(f"{username} disconnected from {topic}")
#         if topic in topic_users:
#             topic_users[topic].pop(username, None)
#             if not topic_users[topic]:
#                 topic_users.pop(topic, None)
#                 topic_messages.pop(topic, None)

#     except Exception as e:
#         print(f"General error: {e}")
#         try:
#             await websocket.send_json({"error": str(e)})
#             await websocket.close(code=4000)
#         except:
#             pass

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
