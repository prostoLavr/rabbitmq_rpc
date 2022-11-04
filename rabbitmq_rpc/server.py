import json
import logging
from typing import Callable

import pika


logger = logging.getLogger("rabbitmq_rpc")
logger.setLevel(logging.DEBUG)


def declare_to_receive(rabbit_url: str, queue: str, func: Callable):
    connection = pika.BlockingConnection(
        pika.URLParameters(rabbit_url)
    )

    channel = connection.channel()

    channel.queue_declare(queue=queue)

    def on_request(ch, method, props, body: bytes):
        request = json.loads(body)
        logger.debug(f'got request: {request}')
        try:
            response = func(request)
            if response is None:
                response = {'success': True}
            if not isinstance(response, dict | list):
                raise TypeError('Function result musts be dict or list')
            if 'success' not in response.keys():
                response.update({'success': True})
            answer = json.dumps(response)
        except Exception as e:
            logger.exception(e)
            response = {'success': False, 'error': e.__class__.__name__}
            answer = json.dumps(response)

        logger.debug(f'send answer: {answer}')

        ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=answer)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=on_request)

    logger.info("start")
    channel.start_consuming()


def example():
    """Work example"""
    rabbit_url = "amqp://guest:guest@localhost/?connection_attempts=5&" \
                 "retry_delay=5&blocked_connection_timeout=420"
    queue = 'calculate_fib'

    def fib(n: int):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    def fib_from_request(request: dict):
        return {'answer': fib(request['value'])}

    declare_to_receive(rabbit_url, queue, fib_from_request)


if __name__ == "__main__":
    logger.info('start')
    example()

