import pika
import os
import time
import sys


def receive_message():
    def callback(ch, method, body, *args, **kwargs):
        print(f"[X] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='hello',
        on_message_callback=callback
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        receive_message()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
