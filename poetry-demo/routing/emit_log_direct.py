import pika
import sys


def emit_log_direct():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # channel.queue_declare(queue='hello')
    channel.exchange_declare(
        exchange='direct_logs',
        exchange_type='direct'
    )

    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = b' '.join(sys.argv[2:]) or b'Hello World!'

    channel.basic_publish(
        exchange='direct_logs',
        routing_key=severity,
        body=message
    )

    print(f"[X] Sent {severity}:{message}")
    connection.close()


if __name__ == "__main__":
    emit_log_direct()
