import pika, sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello_queue')  # 在producer的程式我們已經declare queue，所以這行其實沒作用，重複CALL沒關係，就確保hello queue一定有

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello_queue', on_message_callback=callback, auto_ack=True)   # 註冊 callback 到 queue，收到 message 會跑 callback function

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()    # never-ending loop


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
