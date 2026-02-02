#!/usr/bin/env bash
set -e

START_DATE=$1
END_DATE=$2

if [[ -z "$START_DATE" || -z "$END_DATE" ]]; then
  echo "Usage: backfill_job.sh <start_date> <end_date>"
  exit 1
fi

spark-submit \
  --master spark://spark-master:7077 \
  --name render-telemetry-backfill \
  spark/batch_dimensions.py \
  --start-date ${START_DATE} \
  --end-date ${END_DATE}
