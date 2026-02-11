#!/bin/bash

# replay_kafka_topic.sh
#
# Replays a Kafka topic from earliest offset.
#
# Usage:
#   ./replay_kafka_topic.sh render-events localhost:9092

TOPIC=$1
BROKERS=$2

if [ -z "$TOPIC" ]; then
  echo "Usage: $0 <topic> <brokers>"
  exit 1
fi

if [ -z "$BROKERS" ]; then
  BROKERS="localhost:9092"
fi

echo "Replaying topic: $TOPIC"
echo "Brokers: $BROKERS"

kafka-console-consumer \
  --bootstrap-server "$BROKERS" \
  --topic "$TOPIC" \
  --from-beginning
