# Apache Zookeeper

使用 Apache Zookeeper 實現 Service Discovery 與負載均衡

以 docker compose 模擬下面的叢集：

1. Zookeeper
2. app service：從 Zookeeper 取得當前運行中的 worker 資料
3. worker service：啟動時會註冊到 Zookeeper

客戶端從 app 那取得對應的 worker，app 會選擇當前連線數少的 worker 優先推薦


操作：
- 使用 curl localhost:8000/nodes 取得當前 worker 連線數
- ws://localhost:9000/connect 連線到 worker1


# Apache Zookeeper 介紹

Apache Zookeeper 是一個軟體，主要功用是在分散式系統中提供協調各個 Node 的服務，像是負載均衡、分佈式鎖、Master選舉、命名服務 (Naming Service) 等


## Zookeeper 元件構成：

1. Client：客端
2. Server：在 Zookeeper ensemble 中的一個 node，為 Client 提供服務
3. Ensemble：Server 集合，至少要三個 Server Node 才可成一 Ensemble
4. Leader：負責統整指揮的 Server Node
5. Follower：會聽從 Leader Node 指令的 Server Node


## API

Zookeeper 會維護一個類似文件系統的多階層的命名空間，分佈式的進程透過這個共享的命名空間來進行協調

Zookeeper 提供幾個 API 讓 Client 能操作與更新 Zookeeper 的命名空間

- connect
- create
- delete
- exists
- getData
- setData
- getChildren
- close
