import pika
import sys


def emit_log():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # channel.queue_declare(queue='hello')
    channel.exchange_declare(
        exchange='logs',
        exchange_type='fanout'
    )

    message = b' '.join(sys.argv[1:]) or b'info: Hello World!'
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=message
    )

    print(f"[X] Sent {message}")
    connection.close()


if __name__ == "__main__":
    emit_log()
