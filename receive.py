import json, sys, os

import constants
from utils import sendMessage
from mq import RabbitMQChannel
from summary import generateSummary

rabbitmq = RabbitMQChannel()
channel = rabbitmq.get_channel()


def check_keys_exist(dictionary, keys_to_check):
    missing_keys = [key for key in keys_to_check if key not in dictionary]

    if missing_keys:
        missing_keys_str = ", ".join(missing_keys)
        raise KeyError(
            f"The following key(s) do not exist in the dictionary: {missing_keys_str}"
        )

    return True


def callback(ch, method, properties, body):
    try:
        inputParams = json.loads(body)
        check_keys_exist(inputParams, ["fileName", "columnName", "modelName"])

        print(inputParams)
        summary = generateSummary(
            fileName = inputParams.get('fileName'),
            columnName = inputParams.get('columnName'),
            modelName = inputParams.get('modelName')
        )

        print(summary)
        sendMessage({ 'summary': summary }, constants.ROUTING_OUTPUT_QUEUE)
    except Exception as e:
        print(str(e))
        sendMessage({ 'error': str(e) }, constants.ROUTING_OUTPUT_QUEUE)


def main():
    channel.basic_consume(
        queue=constants.ROUTING_INPUT_QUEUE, auto_ack=True, on_message_callback=callback
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        channel.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
