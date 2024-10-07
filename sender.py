from typing import List

from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, KafkaError

import core

conf = {'bootstrap.servers': core.kafka_broker,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': core.kafka_api_key,
        'sasl.password': core.kafka_api_secret,
        'message.max.bytes': 8388608,
        'client.id': 'integrations_singapore'}


def send_batch(topic: str, data: List[bytes]):
    try:
        producer = Producer(conf)
        for message in data:
            producer.produce(topic, message)
        producer.flush()
    except Exception as ex:
        print (f'produce failed {ex}')
        return
    print (f'batch of {len(data)} produced')


def truncate_topic(topic: str, partitions: int = 2):
    admin_client = AdminClient(conf)
    future = admin_client.delete_topics([topic])
    try:
        future[topic].result()
    except KafkaException as kafka_error:
        pass
    new_topic = NewTopic(topic, partitions)
    admin_client.create_topics([new_topic])
