from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
rooms = {}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    room = await ws.receive_text()
    rooms.setdefault(room, []).append(ws)

    try:
        while True:
            msg = await ws.receive_text()
            for client in rooms[room]:
                if client != ws:
                    await client.send_text(msg)
    except WebSocketDisconnect:
        rooms[room].remove(ws)
