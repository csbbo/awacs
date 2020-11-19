# AWACS


websocket测试
```javascript
ws = new WebSocket('ws://127.0.0.1:8002/ws/')
ws.onmessage = event => console.log(event.data)
ws.send("ping")
```