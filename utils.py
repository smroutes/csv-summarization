import json

from mq import RabbitMQChannel


def sendMessage(messageBody, route):
    rabbitmq = RabbitMQChannel()
    channel = rabbitmq.get_channel()

    channel.basic_publish(
        exchange="", routing_key=route, body=json.dumps(messageBody)
    )

    print(f"Message sent to {route}")
