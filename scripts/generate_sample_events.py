#!/usr/bin/env python3

"""
generate_sample_events.py

Simulates render farm telemetry events and optionally publishes to Kafka.

Usage:
    python generate_sample_events.py --count 10000
    python generate_sample_events.py --count 10000 --kafka --brokers localhost:9092
"""

import json
import uuid
import time
import random
import argparse
from datetime import datetime, timezone
from typing import Dict

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None


SCENES = [f"scene_{i}" for i in range(1, 51)]
NODES = [f"node_{i}" for i in range(1, 101)]


def generate_event() -> Dict:
    scene_id = random.choice(SCENES)

    # Simulate skew (popular scenes)
    if random.random() < 0.2:
        scene_id = "scene_hot_1"

    return {
        "frame_id": str(uuid.uuid4()),
        "scene_id": scene_id,
        "node_id": random.choice(NODES),
        "render_time_ms": random.randint(5000, 40000),
        "gpu_utilization": round(random.uniform(0.4, 0.99), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def create_producer(brokers: str):
    if KafkaProducer is None:
        raise RuntimeError("kafka-python not installed. pip install kafka-python")

    return KafkaProducer(
        bootstrap_servers=brokers.split(","),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=10,
        acks="all"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--kafka", action="store_true")
    parser.add_argument("--brokers", default="localhost:9092")
    parser.add_argument("--topic", default="render-events")
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    producer = None
    if args.kafka:
        producer = create_producer(args.brokers)

    for _ in range(args.count):
        event = generate_event()

        if producer:
            producer.send(args.topic, event)
        else:
            print(json.dumps(event))

        if args.sleep > 0:
            time.sleep(args.sleep)

    if producer:
        producer.flush()
        producer.close()

    print(f"Generated {args.count} events")


if __name__ == "__main__":
    main()
