#!/usr/bin/env python3 -u
import os
from datetime import datetime, timezone

from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from watchdog.observers.polling import PollingObserver

from core import photo_schema, kafka_topic, schema_id, PROJECT_ROOT_DIR
from encoder import encode_batch
from sender import send_batch


class PhotoHandler(FileSystemEventHandler):
    start_id = 1000

    def on_created(self, event) -> None:
        if not isinstance(event, FileCreatedEvent):
            return
        if not event.src_path.endswith('.jpg')  and not event.src_path.endswith('.jpeg'):
            print (f'{event.src_path} is not a JPEG file, ignoring')
            return
        file_name  =  os.path.basename(event.src_path)
        print (f'reading {file_name} image from disk')
        try:
            with open(event.src_path, mode='rb') as file:  # b is important -> binary
                data = file.read()
        except Exception as ex:
            print (f'failed to read image data: {ex}')
            return
        self.start_id += 1
        record = {'image_id': self.start_id,
                'timestamp': datetime.now(tz=timezone.utc),
                'path': file_name,
                'content': data
                }
        batch = encode_batch(photo_schema, schema_id, [record])
        print (f'sending {file_name} to Kafka producer')
        send_batch(kafka_topic, batch)


def watch():
    observer = PollingObserver(timeout=.5)
    observer.schedule(PhotoHandler(), f'{PROJECT_ROOT_DIR}/upload')
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    watch()