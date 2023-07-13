import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))  # 首先，建立與RabbitMQ server間的連線

channel = connection.channel()   # 打開 channel 連線


channel.queue_declare(queue='hello_queue')
channel.exchange_declare(exchange='delay')
channel.queue_bind(queue='hello_queue', exchange='delay', routing_key='delay_key')
channel.queue_declare(
    queue='delay_queue',
    arguments={
        'x-dead-letter-exchange': 'delay',
        'x-dead-letter-routing-key': 'delay_key'
    }
)

channel.basic_publish(
    exchange='',
    routing_key='delay_queue',
    body='Hello World!',
    properties=pika.BasicProperties(
        expiration='10000',  # 10s
    )
)

connection.close()   # 關閉連線，也確保network buffer flush
