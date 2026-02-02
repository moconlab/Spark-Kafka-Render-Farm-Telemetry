from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("RenderTelemetryBatchDims").getOrCreate()

input_path = "metrics/raw/*.json"
output_path = "metrics/dimensions/"

df = spark.read.json(input_path)

dim_render_node = (
    df.select("render_node")
    .distinct()
    .withColumn("render_node_id", monotonically_increasing_id())
)

dim_scene = (
    df.select("scene")
    .distinct()
    .withColumn("scene_id", monotonically_increasing_id())
)

dim_render_node.write.mode("overwrite").parquet(output_path + "render_nodes")
dim_scene.write.mode("overwrite").parquet(output_path + "scenes")
