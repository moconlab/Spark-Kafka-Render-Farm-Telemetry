from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("RenderTelemetryOptimized")
    .config("spark.sql.shuffle.partitions", "12")
    .config("spark.sql.streaming.stateStore.providerClass",
            "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
    .getOrCreate()
)

schema = StructType([
    StructField("event_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("render_node", StringType()),
    StructField("scene", StringType()),
    StructField("frame", IntegerType()),
    StructField("gpu_util", DoubleType()),
    StructField("cpu_util", DoubleType()),
    StructField("mem_util", DoubleType()),
    StructField("render_time_ms", IntegerType()),
    StructField("error", StringType())
])

raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "render-telemetry")
    .option("maxOffsetsPerTrigger", 5000)
    .load()
)

parsed = (
    raw.select(from_json(col("value").cast("string"), schema).alias("d"))
       .select("d.*")
       .withColumn("event_time", to_timestamp("timestamp"))
       .withWatermark("event_time", "2 minutes")
)

# Narrow aggregation with pruning
agg = (
    parsed.groupBy(
        window("event_time", "1 minute"),
        "render_node"
    )
    .agg(
        avg("gpu_util").alias("avg_gpu"),
        avg("cpu_util").alias("avg_cpu"),
        avg("render_time_ms").alias("avg_render_ms"),
        count("*").alias("frames")
    )
)

query = (
    agg.writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", False)
    .option("checkpointLocation", "metrics/checkpoints/render")
    .start()
)

query.awaitTermination()
