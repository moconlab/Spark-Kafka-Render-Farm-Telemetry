# Optimization Notes

This document captures performance and reliability optimizations applied
throughout the pipeline.

## Kafka Optimizations

- Adequate partition count to match Spark parallelism
- Compression enabled (lz4 or snappy)
- Batching tuned via producer linger and batch size
- Retention aligned with reprocessing requirements

## Spark Streaming Optimizations

### Execution Model
- Micro-batch mode with short batch intervals
- Backpressure enabled
- Controlled max offsets per trigger

### State Management
- Event-time watermarks to bound state
- State TTL tuned per aggregation
- Avoid wide state keys

### Shuffle Reduction
- Pre-aggregation before joins
- Repartitioning on natural keys
- Broadcast joins for small dimension tables

## Storage Optimizations

### Delta Lake
- Partition by date and low-cardinality dimensions
- Periodic OPTIMIZE and ZORDER
- Compact small files via auto-optimize

### Parquet
- Larger file sizes to reduce metadata overhead
- Snappy compression for balanced CPU / IO usage

## Cost & Stability Considerations

- Checkpoint directories isolated per job
- Separate raw and aggregated storage paths
- Idempotent writes prevent duplication on retries

## Trade-offs

- Lower latency increases state pressure
- Longer retention increases Kafka storage cost
- Finer partitions improve parallelism but increase metadata
