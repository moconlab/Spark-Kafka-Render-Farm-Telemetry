#!/bin/bash

KAFKA_BROKER=localhost:9092
TOPIC=render-telemetry

kafka-topics.sh \
  --bootstrap-server $KAFKA_BROKER \
  --create \
  --topic $TOPIC \
  --partitions 6 \
  --replication-factor 1 \
  --if-not-exists

kafka-topics.sh \
  --bootstrap-server $KAFKA_BROKER \
  --describe \
  --topic $TOPIC
