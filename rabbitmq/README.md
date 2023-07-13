# RabbitMQ

實作延遲 queue

建立一個 queue (這裡我們命名為 delay_queue)，delay_queue 不會設定有 consumer 監聽訊息，到這 queue 的訊息會等到過期透過 dead letter exhange 轉去另一個 queue (名字為 hello_queue)
consumer 接收 hello_queue 的訊息，過期的訊息到 hello_queue 就會被消耗
如此可以達成延遲接收訊息的功能


操作：
1. docker compose up 啟動 rabbitmq
2. python3 producer.py
3. python3 consumer.py


# Exchange

訊息的傳遞要先送到 Exchange ，由 Exhange 才轉送到 Queue 中

Exchange 有四種：

## 1. Direct

Producer 透過設定 routing_key 的方式，將消息傳到特定 queue 或是同時多個 queue

Direct Exchange 會傳給與 Producer 帶的 routing_key 字串完全符合的 binding routing_key 對應的 queue 裡


##  2. Fanout

Fanout Exchange 會發送消息到他所知道的所有 queue，不會看 routing_key


## 3. Topic

Topic Exchange 跟 Direct Exchange 差不多，但可以在 binding routing_key 裡使用 wildcard


## 4. Headers

Header Exchange 則會看消息的 header 值來決定要傳到哪些Queue
