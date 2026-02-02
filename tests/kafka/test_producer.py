from kafka import KafkaProducer
import json

def test_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    future = producer.send(
        "render.telemetry.raw",
        {"render_node_id": "test-node", "latency_ms": 123}
    )

    record_metadata = future.get(timeout=10)
    assert record_metadata.topic == "render.telemetry.raw"
