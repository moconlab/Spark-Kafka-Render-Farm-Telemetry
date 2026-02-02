from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def spark():
    return (
        SparkSession.builder
        .master("local[2]")
        .appName("test-aggregations")
        .getOrCreate()
    )

def test_basic_aggregation():
    spark_session = spark()

    data = [
        ("node1", 100),
        ("node1", 200),
        ("node2", 50),
    ]

    df = spark_session.createDataFrame(
        data, ["render_node_id", "latency_ms"]
    )

    agg = (
        df.groupBy("render_node_id")
        .avg("latency_ms")
        .collect()
    )

    result = {row["render_node_id"]: row["avg(latency_ms)"] for row in agg}
    assert result["node1"] == 150
