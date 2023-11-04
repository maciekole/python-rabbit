import pika
import sys


def emit_log_topic():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # channel.queue_declare(queue='hello')
    channel.exchange_declare(
        exchange='topic_logs',
        exchange_type='topic'
    )

    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    message = b' '.join(sys.argv[2:]) or b'Hello World!'

    channel.basic_publish(
        exchange='topic_logs',
        routing_key=routing_key,
        body=message
    )

    print(f"[X] Sent {routing_key}:{message}")
    connection.close()


if __name__ == "__main__":
    emit_log_topic()
