# Redis

使用 Redis Pub/Sub 實作聊天室

Nginx + FastAPI + Redis Pub/Sub


操作：
- ws://localhost:8000/chat 連上伺服器
- 傳送 {"type": "CREATE", "name": "player1"} 可以建立新的聊天室 (聊天室有獨特的uuid)
- 傳送 {"type": "JOIN", "name": "player2", "room": "7d47a640-4147-4d5f-9383-88950ec1b125"} 可以加入聊天室
- 傳送 {"type": "PUBLISH", "message": "hello"} 發送訊息到聊天室
- 傳送 {"type": "LEAVE"} 離開聊天室


# Screenshots

![image](https://github.com/wovex/services/blob/master/redis/imgs/chat_test.png)
