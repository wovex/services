# Grafana

Grafana 是開源的資料視覺化工具

Grafana docker image 預設帳密: admin / admin


Grafana 內建支援各種 Data source，我們這裡使用 Prometheus 和 Loki 做為資料來源

Prometheus 設定定時去抓 fastapi server 和 node exporter 的 metrics

使用 Promtail 將 fastapi server 裡的 log 送到 Loki



參考：
- https://grafana.com/tutorials/grafana-fundamentals/?utm_source=grafana_gettingstarted


## Prometheus 設定

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: 'fastapi-app'
    scrape_interval: 10s
    metrics_path: /metrics
    static_configs:
      - targets: ['fastapi-app:5000']

  - job_name: 'node'
    scrape_interval: 10s
    metrics_path: /metrics
    static_configs:
      - targets: ['fastapi-app:9100']
```

## Promtail 設定

```yaml
clients:
- url: 'http://loki:3100/loki/api/v1/push'

scrape_configs:
 - job_name: fastapi
   pipeline_stages:
   static_configs:
   - targets:
      - localhost
     labels:
      __path__: /var/log/app.log*

```
