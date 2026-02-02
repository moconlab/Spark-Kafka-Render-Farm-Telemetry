#!/usr/bin/env bash
set -e

APP_NAME="render-telemetry-streaming"
SPARK_MASTER=${SPARK_MASTER:-"spark://spark-master:7077"}
CHECKPOINT_DIR=${CHECKPOINT_DIR:-"/checkpoints/render-telemetry"}

spark-submit \
  --master ${SPARK_MASTER} \
  --name ${APP_NAME} \
  --conf spark.sql.shuffle.partitions=200 \
  --conf spark.streaming.backpressure.enabled=true \
  --conf spark.sql.streaming.checkpointLocation=${CHECKPOINT_DIR} \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,io.delta:delta-spark_2.12:3.1.0 \
  spark/streaming_optimized.py
