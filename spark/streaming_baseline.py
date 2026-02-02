from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("RenderTelemetryBaseline")
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

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "render-telemetry")
    .load()
)

parsed = (
    df.select(from_json(col("value").cast("string"), schema).alias("data"))
      .select("data.*")
)

# Expensive wide aggregation (no watermark, no pruning)
agg = (
    parsed.groupBy("render_node")
    .avg("gpu_util", "cpu_util", "render_time_ms")
)

query = (
    agg.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()
