import asyncio
import websockets
import json

# async def chat():
#     uri = "ws://localhost:8000/ws"
#     async with websockets.connect(uri) as ws:
#         await ws.send(json.dumps({"username": "alice", "topic": "sports"}))
#         print(await ws.recv())

#         while True:
#             msg = input("Enter message ('/list' to show users, Ctrl+C to exit): ")
#             await ws.send(json.dumps({"msg": msg}))
#             print(await ws.recv())

# asyncio.get_event_loop().run_until_complete(chat())

# import asyncio
# import websockets
# import json

# async def chat():
#     uri = "ws://localhost:8000/ws"
#     username = input("Enter your username: ")
#     topic = input("Enter the room/topic you want to join: ")
#     async with websockets.connect(uri) as ws:
#         await ws.send(json.dumps({"username": username, "topic": topic}))
#         print(await ws.recv())
#         try:
#             while True:
#                 msg = input("Enter message ('/list' to show users, Ctrl+C to exit): ")
#                 await ws.send(json.dumps({"msg": msg}))
#                 print(await ws.recv())
#         except Exception as e:
#             print("Connection closed or error:", e)

# asyncio.get_event_loop().run_until_complete(chat())



# import asyncio
# import websockets
# import json

# async def receive_messages(ws):
#     """Continuously receive messages from the server."""
#     try:
#         async for msg in ws:
#             data = json.loads(msg)
#             if "msg" in data:
#                 # Normal message
#                 print(f"\n{data['msg']}")
#             elif "topics" in data:
#                 # /list response with usernames
#                 print("\nActive topics:")
#                 for topic, info in data["topics"].items():
#                     users_str = ", ".join(info["users"])
#                     print(f"  {topic}: {info['count']} user(s) -> {users_str}")
#             elif "info" in data:
#                 print(f"\n[Info] {data['info']}")
#             elif "error" in data:
#                 print(f"\n[Error] {data['error']}")
#               # Reprint prompt
#             print("Enter message (c to quit, /list to show topics): ", end="", flush=True)
#     except websockets.ConnectionClosed:
#         print("\nConnection closed.")

# async def send_messages(ws):
#     """Continuously read input from the terminal and send to server."""
#     loop = asyncio.get_event_loop()
#     while True:
#         msg = await loop.run_in_executor(None, lambda: input("Enter message: "))
#         if msg.strip().lower() == "exit":
#             print("Exiting...")
#             await ws.close()
#             break
#         await ws.send(json.dumps({"msg": msg}))

# async def chat():
#     uri = "ws://localhost:8000/ws"
#     username = input("Enter your username: ")
#     topic = input("Enter the room/topic you want to join: ")

#     async with websockets.connect(uri) as ws:
#         await ws.send(json.dumps({"username": username, "topic": topic}))
#         print(await ws.recv())

#         await asyncio.gather(
#             receive_messages(ws),
#             send_messages(ws),
#         )

# if __name__ == "__main__":
#     try:
#         asyncio.run(chat())
#     except KeyboardInterrupt:
#         print("\nClient closed.")



import asyncio
import websockets
import json

# async def receive_messages(ws):
#     try:
#         async for msg in ws:
#             data = json.loads(msg)
#             if "msg" in data:
#                 msg_data = data["msg"]
#                 print(f"\n[{msg_data['timestamp']}] {msg_data['username']}: {msg_data['message']}")
#             elif "topics" in data:
#                 print("\nActive topics:")
#                 for topic, count in data["topics"].items():
#                     print(f"  {topic}: {count}")
#             elif "info" in data:
#                 print(f"\n[Info] {data['info']}")
#             elif "error" in data:
#                 print(f"\n[Error] {data['error']}")
#             print("Enter message (c to quit, /list to show topics): ", end="", flush=True)
#     except websockets.ConnectionClosed:
#         print("\nConnection closed.")


import time  # needed to format timestamps

async def receive_messages(ws):
    """Continuously receive messages from the server."""
    try:
        async for msg in ws:
            data = json.loads(msg)
            if "msg" in data:
                msg_data = data["msg"]
                # Convert timestamp to readable format
                ts_readable = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(msg_data['timestamp'])
                )
                print(f"\n[{ts_readable}] {msg_data['username']}: {msg_data['message']}")
            elif "topics" in data:
                print("\nActive topics:")
                for topic, count in data["topics"].items():
                    print(f"  {topic}: {count}")
            elif "info" in data:
                print(f"\n[Info] {data['info']}")
            elif "error" in data:
                print(f"\n[Error] {data['error']}")
            print("Enter message (c to quit, /list to show topics): ", end="", flush=True)
    except websockets.ConnectionClosed:
        print("\nConnection closed.")

async def send_messages(ws):
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(
            None, lambda: input("Enter message (c to quit, /list to show topics): ")
        )
        if msg.strip().lower() == "c":
            print("Exiting...")
            await ws.close()
            break
        await ws.send(json.dumps({"msg": msg}))

async def chat():
    uri = "ws://localhost:8000/ws"
    username = input("Enter your username: ")
    topic = input("Enter the room/topic you want to join: ")

    async with websockets.connect(uri) as ws:
        # Send join payload
        await ws.send(json.dumps({"username": username, "topic": topic}))
        print(await ws.recv())

        await asyncio.gather(
            receive_messages(ws),
            send_messages(ws),
        )

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nClient closed.")





