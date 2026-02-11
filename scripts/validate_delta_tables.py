#!/usr/bin/env python3

"""
validate_delta_tables.py

Validates Delta tables for:
- Row count
- Null checks
- Basic aggregations
- File count sanity
"""

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    spark = (
        SparkSession.builder
        .appName("DeltaValidation")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

    df = spark.read.format("delta").load(args.path)

    print("\n=== Basic Stats ===")
    print(f"Row count: {df.count()}")

    print("\n=== Null Checks ===")
    df.select([
        count(col(c)).alias(c)
        for c in df.columns
    ]).show(truncate=False)

    if "render_time_ms" in df.columns:
        print("\n=== Aggregation Check ===")
        df.groupBy("scene_id") \
            .agg(avg("render_time_ms").alias("avg_render_time")) \
            .orderBy("avg_render_time", ascending=False) \
            .show(10, truncate=False)

    print("\n=== File Count ===")
    file_count = len(df.inputFiles())
    print(f"Underlying data files: {file_count}")

    spark.stop()


if __name__ == "__main__":
    main()
