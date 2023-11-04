import pika
import os
import time
import sys


def receive_logs_topic():
    def callback(ch, method, properties, body, *args, **kwargs):
        print(f"[X] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        receive_logs_topic()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
