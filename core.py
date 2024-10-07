import os
from pathlib import Path

from avro.schema import parse

PROJECT_ROOT_DIR = Path(__file__).parent

with open(f'{PROJECT_ROOT_DIR}/photos.avsc', mode='r') as schema_file:
    photo_schema = parse(schema_file.read())
schema_id = 100084
kafka_topic = 'singapore_photos'
kafka_broker = 'pkc-ymrq7.us-east-2.aws.confluent.cloud:9092'
kafka_api_key = os.getenv('KAFKA_API_KEY')
kafka_api_secret = os.getenv('KAFKA_API_SECRET')
