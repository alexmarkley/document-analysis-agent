#!/bin/bash

set -e

PROJECT_ID=$(gcloud config get-value project)
DATASET_NAME="document_analysis"
TABLE_NAME="results"

SCHEMA="entity_name:STRING,signed_date:DATE,filed_date:DATE"

# Check if the dataset already exists.
if bq show --format=prettyjson "${PROJECT_ID}:${DATASET_NAME}" > /dev/null 2>&1; then
    echo "Dataset '${DATASET_NAME}' already exists. Skipping creation."
else
    echo "Creating dataset '${DATASET_NAME}'..."
    bq --location="US" mk --dataset "${PROJECT_ID}:${DATASET_NAME}"
    echo "Dataset created successfully."
fi

# Check if the table already exists.
if bq show --format=prettyjson "${PROJECT_ID}:${DATASET_NAME}.${TABLE_NAME}" > /dev/null 2>&1; then
    echo "Table '${TABLE_NAME}' already exists. Skipping creation."
else
    echo "Creating table '${TABLE_NAME}'..."
    bq mk --table "${PROJECT_ID}:${DATASET_NAME}.${TABLE_NAME}" "${SCHEMA}"
    echo "Table created successfully."
fi
