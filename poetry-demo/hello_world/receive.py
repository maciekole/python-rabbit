import pika
import os
import sys


def receive_message():
    def callback(body, *args, **kwargs):
        print(f"[X] Received {body}")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_consume(
        queue='hello',
        auto_ack=True,
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
