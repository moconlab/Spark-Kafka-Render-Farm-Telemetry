# System Architecture

This repository implements a real-time telemetry pipeline for Render nodes using
Kafka and Spark Structured Streaming, with optimized aggregations persisted to
Parquet and Delta Lake.

## High-Level Architecture

Render Nodes
    ↓ (events)
Kafka Topics
    ↓
Spark Structured Streaming
    ↓
Optimized Aggregations
    ↓
Parquet / Delta Tables

## Components

### Render Nodes
- Emit telemetry events (frame renders, timings, resource usage)
- Events are JSON or Avro encoded
- Designed for high-throughput, append-only writes

### Kafka
- Acts as the durable ingestion buffer
- Topics partitioned by `render_node_id`
- Enables replay, backfill, and fault tolerance
- Retention configured to allow reprocessing

### Spark Structured Streaming
- Consumes Kafka topics using micro-batch execution
- Applies schema enforcement and validation
- Handles late data via event-time watermarking
- Maintains stateful aggregations

### Aggregation Layer
- Windowed metrics (per node, per job, per time window)
- Stateful rollups for long-running metrics
- Optimized to minimize shuffle and state size

### Storage Layer
- **Parquet** for raw or lightly processed events
- **Delta Lake** for aggregated, query-optimized datasets
- Partitioned by date and logical dimensions

## Failure & Recovery

- Kafka offsets stored in Spark checkpoints
- Checkpoint-backed state enables exactly-once semantics
- Delta Lake provides ACID guarantees for aggregated outputs

## Design Goals

- Horizontal scalability
- Deterministic reprocessing
- Low-latency aggregations
- Operational transparency
