import pika
import sys


def send_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True)

    message = b' '.join(sys.argv[1:]) or b'Hello World!'
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.spec.PERSISTENT_DELIVERY_MODE
    )

    print(f"[X] Sent {message}")
    connection.close()


if __name__ == "__main__":
    send_message()
