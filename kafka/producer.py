import json
import random
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

BROKER = "localhost:9092"
TOPIC = "render-telemetry"

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=5,
    acks="1"
)

RENDER_NODES = [f"render-node-{i}" for i in range(50)]
SCENES = ["city", "forest", "space", "ocean"]
ERRORS = [None, None, None, "GPU_OOM", "DISK_IO", "NETWORK"]

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "render_node": random.choice(RENDER_NODES),
        "scene": random.choice(SCENES),
        "frame": random.randint(1, 10000),
        "gpu_util": round(random.uniform(10, 100), 2),
        "cpu_util": round(random.uniform(5, 95), 2),
        "mem_util": round(random.uniform(20, 98), 2),
        "render_time_ms": random.randint(5, 200),
        "error": random.choice(ERRORS)
    }

if __name__ == "__main__":
    print("Producing render telemetry...")
    while True:
        event = generate_event()
        producer.send(TOPIC, event)
        time.sleep(0.02)  # ~50 events/sec
