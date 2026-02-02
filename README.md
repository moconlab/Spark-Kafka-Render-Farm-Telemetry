# Spark-Kafka-Render-Farm-Telemetry
Render Farm Analytics: Optimizing Spark for VFX Pipelines (Kafka + Spark)

## Overview

Modern VFX studios operate global render farms producing massive volumes of telemetry in real time.
Each render node streams logs capturing performance, hardware utilization, and errors for every rendered frame.

This project simulates a production-grade streaming analytics pipeline using Kafka + Spark Structured Streaming, with a strong emphasis on Spark performance optimization.

The core objective is to demonstrate the ability to:

Design scalable streaming architectures

Diagnose Spark bottlenecks

Apply targeted optimizations using Spark internals knowledge

## Architecture

```
Render Nodes
   ↓ (events)
Kafka Topics
   ↓
Spark Structured Streaming
   ↓
Optimized Aggregations
   ↓
Parquet / Delta Tables
```

## Problem Statement

Render farms emit high-volume events:

- Frame render time
- Scene complexity
- Node hardware usage
- Failure and retry logs

Naive streaming pipelines suffer from:
- High shuffle pressure
- Skewed scene workloads
- Inefficient joins with static metadata
- Expensive recomputation of aggregates

## Data Model
### Kafka Topics

`render-events`
```
{
  "frame_id": "string",
  "scene_id": "string",
  "node_id": "string",
  "render_time_ms": 18234,
  "gpu_utilization": 0.87,
  "timestamp": "2025-01-01T10:15:30Z"
}
```
## Dimension Tables (Batch)

- scenes
- hardware_nodes

Stored as Parquet / Delta and refreshed periodically.

## Key Experiments & Optimizations
### 1. Streaming Join Optimization

Baseline

- Streaming-to-batch joins without broadcast

- High shuffle overhead

Optimized

- Broadcast static dimension tables

- Join reordering

Why It Matters

- Streaming joins magnify shuffle costs

- Broadcast eliminates unnecessary network IO

### 2. Partitioning & State Management

Baseline

- Default partitioning

- Large state stores

Optimized

- Keyed aggregations by scene_id

- Tuned spark.sql.shuffle.partitions

- Reduced state size

### 3. Windowed Aggregations

Baseline

- Wide time windows

- Large state retention

Optimized

- Sliding vs tumbling windows

- Watermarks to limit state growth

`.withWatermark("timestamp", "10 minutes")`

### 4. Skew Detection & Mitigation

Baseline

- Popular scenes dominate processing time

Optimized

- Scene bucketing

- AQE enabled

- Skew-aware repartitioning

### 5. Caching Static Data

Baseline

- Repeated reads of scene metadata

Optimized

- Cached broadcast dimension tables

- MEMORY_AND_DISK persistence

## Performance Measurement

Metrics collected:

- End-to-end latency

- Micro-batch duration

- Shuffle read/write

- State store size

Measured via:

- Spark UI (Streaming tab)

- Structured Streaming metrics

## Results (example)

| Optimization   | Before | After | Improvement |
| -------------- | ------ | ----- | ----------- |
| Batch Duration | 90s    | 18s   | 5×          |
| Shuffle Size   | 6.2GB  | 500MB | 12×         |
| State Store    | 3.5GB  | 900MB | 4×          |

## Tech Stack

- Apache Kafka

- PySpark

- Spark Structured Streaming

- Parquet / Delta Lake

- Databricks or Local Spark

## Repo Structure
```
spark-kafka-render-telemetry/
├── kafka/
│   ├── producer.py
│   ├── topic_setup.sh
│   ├── schemas/
│   │   ├── render_event.avsc
│   │   └── aggregation_event.avsc
│   └── consumer_smoke_test.py
│
├── spark/
│   ├── streaming_baseline.py
│   ├── streaming_optimized.py
│   ├── batch_dimensions.py
│   ├── aggregations/
│   │   ├── windowed_metrics.py
│   │   ├── stateful_rollups.py
│   │   └── watermarking.py
│   ├── sinks/
│   │   ├── delta_sink.py
│   │   └── parquet_sink.py
│   └── checkpoints/
│       └── README.md
│
├── storage/
│   ├── delta/
│   │   ├── render_metrics/
│   │   └── aggregated_metrics/
│   └── parquet/
│       └── raw_events/
│
├── orchestration/
│   ├── spark_submit.sh
│   ├── backfill_job.sh
│   └── cron_example.txt
│
├── metrics/
│   ├── spark_metrics.json
│   ├── kafka_lag_exporter.yml
│   └── prometheus_rules.yml
│
├── config/
│   ├── spark.conf
│   ├── kafka.conf
│   └── env.example
│
├── tests/
│   ├── kafka/
│   │   └── test_producer.py
│   ├── spark/
│   │   └── test_aggregations.py
│   └── integration/
│       └── test_end_to_end.py
│
├── docker/
│   ├── docker-compose.yml
│   ├── spark.Dockerfile
│   └── kafka.Dockerfile
│
├── scripts/
│   ├── generate_sample_events.py
│   ├── validate_delta_tables.py
│   └── replay_kafka_topic.sh
│
├── docs/
│   ├── architecture.md
│   ├── data_flow.md
│   └── optimization_notes.md
│
├── .gitignore
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md

```

