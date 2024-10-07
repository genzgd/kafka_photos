#!/usr/bin/env python3 -u

from datetime import datetime, timezone

from core import photo_schema, kafka_topic, schema_id
from encoder import encode_batch
from sender import truncate_topic, send_batch


def send_seeds():
    truncate_topic(kafka_topic)
    if datetime.now().timestamp() > 0:
        return
    seeds = []
    for ix in range(10):
        data = {'image_id': ix,
                'timestamp': datetime.now(tz=timezone.utc),
                'path': f'/seed/{ix}',
                'content': f'This would be photo {ix}'.encode('utf-8')}
        seeds.append(data)
    seed_data = encode_batch(photo_schema, schema_id, seeds)
    send_batch(kafka_topic, seed_data)


if __name__ == '__main__':
    send_seeds()