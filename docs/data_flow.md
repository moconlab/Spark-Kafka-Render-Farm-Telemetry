# Data Flow

This document describes how telemetry data moves through the system from
Render nodes to analytical storage.

## 1. Event Production

Render nodes generate telemetry events containing:
- Event timestamp
- Render node ID
- Job or frame identifier
- Performance metrics (latency, CPU, memory, GPU usage)

Events are serialized and published to Kafka topics.

## 2. Kafka Ingestion

- Topics are partitioned by render node ID
- Producers use idempotent writes
- Retention allows multi-day replay for backfills

Example topic:
- `render.telemetry.raw`

## 3. Spark Structured Streaming

Spark streaming jobs:
1. Read from Kafka
2. Parse and validate schemas
3. Apply event-time semantics
4. Drop or redirect malformed records
5. Apply windowed and stateful aggregations

Watermarks are used to bound state and handle late arrivals.

## 4. Aggregation Logic

Typical aggregations include:
- Per-node metrics per minute
- Per-job render duration summaries
- Percentiles over sliding windows

Aggregations are computed incrementally to avoid full recomputation.

## 5. Storage

### Raw Events
- Written to Parquet
- Partitioned by ingestion date
- Used for reprocessing and audits

### Aggregated Metrics
- Written to Delta Lake
- Partitioned by event date
- Optimized for downstream analytics and dashboards

## 6. Consumption

Downstream systems (BI tools, ad-hoc Spark jobs):
- Read Delta tables for fast queries
- Rely on schema evolution and ACID guarantees
