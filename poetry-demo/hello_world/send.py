import pika


def send_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=b'Hello world!'
    )

    print("[X] Sent 'Hello world!'")
    connection.close()


if __name__ == "__main__":
    send_message()
