import io
from typing import Dict, List

from avro.io import BinaryEncoder, DatumWriter
from avro.schema import Schema


def encode_batch(avro_schema: Schema, schema_id: int, records:List[Dict]):
    results = []
    writer = DatumWriter(avro_schema)
    for record in records:
        buf = io.BytesIO()
        encoder = BinaryEncoder(buf)
        writer.write(record, encoder)
        buf.seek(0)
        byte_record = bytearray(0)
        byte_record.append(0)
        byte_record.extend(schema_id.to_bytes(4, 'big'))
        byte_record.extend(buf.read())
        results.append(bytes(byte_record))
    return results