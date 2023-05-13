# Common
GCP_PROJECT = "GCP_PROJECT"
PROJECT = "PROJECT"
REGION = "REGION"
GCS_STAGING_LOCATION = "GCS_STAGING_LOCATION"
SUBNET = "SUBNET"
IS_PARAMETERIZED = "IS_PARAMETERIZED"
MAX_PARALLELISM =  "MAX_PARALLELISM"
SERVICE_ACCOUNT = "SERVICE_ACCOUNT"

# Write modes
OUTPUT_MODE_OVERWRITE = "overwrite"
OUTPUT_MODE_APPEND = "append"


# MYSQL TO SPANNER
## Command Line Arguments
OUTPUT_NOTEBOOK_ARG = "output.notebook"
MAX_PARALLELISM_ARG = "max.parallelism"
MYSQL_HOST_ARG = "mysql.host"
MYSQL_PORT_ARG = "mysql.port"
MYSQL_USERNAME_ARG = "mysql.username"
MYSQL_PASSWORD_ARG = "mysql.password"
MYSQL_DATABASE_ARG = "mysql.database"
MYSQLTABLE_LIST_ARG = "mysql.table.list"
MYSQL_OUTPUT_SPANNER_MODE_ARG = "mysql.output.spanner.mode"
SPANNER_INSTANCE_ARG = "spanner.instance"
SPANNER_DATABASE_ARG = "spanner.database"
# provide table & pk column which do not have PK in MYSQL "{"table_name":"primary_key"}"
SPANNER_TABLE_PRIMARY_KEYS_ARG = "spanner.table.primary.keys"

## Notebook Arguments
MYSQL_HOST = "MYSQL_HOST"
MYSQL_PORT = "MYSQL_PORT"
MYSQL_USERNAME = "MYSQL_USERNAME"
MYSQL_PASSWORD = "MYSQL_PASSWORD"
MYSQL_DATABASE = "MYSQL_DATABASE"
MYSQLTABLE_LIST = "MYSQLTABLE_LIST"
MYSQL_OUTPUT_SPANNER_MODE = "MYSQL_OUTPUT_SPANNER_MODE"
SPANNER_INSTANCE = "SPANNER_INSTANCE"
SPANNER_DATABASE = "SPANNER_DATABASE"
SPANNER_TABLE_PRIMARY_KEYS = "SPANNER_TABLE_PRIMARY_KEYS"


# HIVE TO BIGQUERY
## Command Line Arguments
HIVE_METASTORE_ARG = "hive.metastore"
INPUT_HIVE_DATABASE_ARG = "input.hive.database"
INPUT_HIVE_TABLES_ARG = "input.hive.tables"
OUTPUT_BIGQUERY_DATASET_ARG = "output.bigquery.dataset"
TEMP_BUCKET_ARG = "temp.bucket"
HIVE_OUTPUT_MODE_ARG = "hive.output.mode"

## Notebook Arguments
HIVE_METASTORE = "HIVE_METASTORE"
INPUT_HIVE_DATABASE = "INPUT_HIVE_DATABASE"
INPUT_HIVE_TABLES = "INPUT_HIVE_TABLES"
OUTPUT_BIGQUERY_DATASET = "OUTPUT_BIGQUERY_DATASET"
TEMP_BUCKET = "TEMP_BUCKET"
HIVE_OUTPUT_MODE = "HIVE_OUTPUT_MODE"
