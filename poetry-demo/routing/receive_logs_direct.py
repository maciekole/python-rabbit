import pika
import os
import time
import sys


def receive_logs():
    def callback(ch, method, properties, body, *args, **kwargs):
        print(f"[X] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        receive_logs()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
