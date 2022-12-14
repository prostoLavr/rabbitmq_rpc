#!/usr/bin/env python
import uuid
import json
import time
from typing import Optional
import logging

import pika


logger = logging.getLogger("rabbitmq")
logger.setLevel(logging.DEBUG)



class RpcClientWorker:
    def __init__(self, connection: pika.BlockingConnection, to_queue: str, 
                 answer_queue: Optional[str] = None, wait_time=1):
        self.to_queue = to_queue
        self.connection = connection
        self.channel = self.connection.channel()
        self.wait_time = wait_time
        
        if answer_queue is None:
            result = self.channel.queue_declare(queue='', exclusive=True)
        else: 
            result = self.channel.queue_declare(queue=answer_queue)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body: bytes):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, body: dict, wait_time=None) -> Optional[dict]:
        if wait_time is None:
            wait_time = self.wait_time
        self.response = None
        self.corr_id = str(uuid.uuid4())
        body = json.dumps(body).encode('utf-8')
        self.channel.basic_publish(
            exchange='',
            routing_key=self.to_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=body)
        while self.response is None:
            self.connection.process_data_events()
            time.sleep(wait_time)
        return self.response


class RpcClient:
    def __init__(self, rabbit_url: str, to_queue: str, 
                 answer_queue: Optional[str] = None, wait_time = 1):
        self.connection = self.__create_connection(rabbit_url)
        self.to_queue = to_queue
        self.answer_queue = answer_queue
        self.wait_time = wait_time

    def __create_connection(self, rabbit_url: str):
        while True:
            try:
                return pika.BlockingConnection(pika.URLParameters(rabbit_url))
            except (pika.exceptions.AMQPConnectorSocketConnectError, 
                    pika.exceptions.AMQPConnectionError): 
                logger.warning('Connection error, '
                               'try to reconnect in 3 seconds')
                time.sleep(3)


    def call(self, body: dict) -> Optional[dict]:
        return RpcClientWorker(self.connection, 
                               self.to_queue, 
                               self.answer_queue, 
                               wait_time=self.wait_time).call(body)


def example():
    """Work example"""
    rabbit_url = "amqp://guest:guest@localhost/?connection_attempts=" \
                 "5&retry_delay=5&blocked_connection_timeout=420"
    queue = 'calculate_fib'

    fib_rpc_client = RpcClient(rabbit_url, queue)
# 
#     logger.info('Waiting server in 15 secs')
#     time.sleep(15)
    logger.info('Begin sending requests')

    for value in (28, 29, 30):
        request_form = {'value': value}
        logger.info(f"send request {request_form}")
        response = fib_rpc_client.call(request_form)
        logger.info(f"got answer {response} for {request_form}")


if __name__ == "__main__":
    example()

