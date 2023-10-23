import pika
import constants


class RabbitMQChannel:
    """
    RabbitMQChannel Singleton

    This class provides a Singleton pattern implementation for a RabbitMQ channel, ensuring that only one channel instance is created. It utilizes the pika library to establish a connection and create a channel. The RabbitMQ channel can be accessed using the 'get_channel' method.

    Attributes:
    _instance: Singleton instance of the RabbitMQChannel.
    connection: A pika BlockingConnection to the RabbitMQ server.
    channel: The RabbitMQ channel for communication.
    ROUTING_INPUT_QUEUE: The name of the routing queue for message handling.

    Methods:
    get_channel(): Returns the RabbitMQ channel for communication.

    Usage:
    rabbitmq_channel = RabbitMQChannel()
    channel = rabbitmq_channel.get_channel()
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQChannel, cls).__new__(cls)
            cls._instance._create_channel()
        return cls._instance

    def _create_channel(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()

        self.ROUTING_INPUT_QUEUE = constants.ROUTING_INPUT_QUEUE
        self.channel.queue_declare(self.ROUTING_INPUT_QUEUE)

        self.ROUTING_OUTPUT_QUEUE = constants.ROUTING_OUTPUT_QUEUE
        self.channel.queue_declare(self.ROUTING_OUTPUT_QUEUE)

    def get_channel(self):
        return self.channel
