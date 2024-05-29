# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, Sequence, Optional, Any
from logging import Logger
import argparse
import pprint

from pyspark.sql import SparkSession

from dataproc_templates import BaseTemplate
from dataproc_templates.util.argument_parsing import add_es_spark_connector_options
from dataproc_templates.util.dataframe_reader_wrappers import ingest_dataframe_from_elasticsearch
from dataproc_templates.util.elasticsearch_transformations import flatten_struct_fields, flatten_array_fields
import dataproc_templates.util.template_constants as constants


__all__ = ['ElasticsearchToBQTemplate']

class ElasticsearchToBQTemplate(BaseTemplate):
    """
    Dataproc template implementing exports from Elasticsearch to BigQuery
    """

    @staticmethod
    def parse_args(args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()

        parser.add_argument(
            f'--{constants.ES_BQ_INPUT_NODE}',
            dest=constants.ES_BQ_INPUT_NODE,
            required=True,
            help='Elasticsearch Node Uri'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_INPUT_INDEX}',
            dest=constants.ES_BQ_INPUT_INDEX,
            required=True,
            help='Elasticsearch Index Name'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_NODE_USER}',
            dest=constants.ES_BQ_NODE_USER,
            required=True,
            help='Elasticsearch Node User'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_NODE_PASSWORD}',
            dest=constants.ES_BQ_NODE_PASSWORD,
            required=True,
            help='Elasticsearch Node Password'
        )

        add_es_spark_connector_options(parser, constants.get_es_spark_connector_input_options("es.bq.input."))

        parser.add_argument(
            f'--{constants.ES_BQ_FLATTEN_STRUCT}',
            dest=constants.ES_BQ_FLATTEN_STRUCT,
            action='store_true',
            required=False,
            help='Flatten the struct fields'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_FLATTEN_ARRAY}',
            dest=constants.ES_BQ_FLATTEN_ARRAY,
            action='store_true',
            required=False,
            help=f'Flatten the n-D array fields to 1-D array fields, it needs {constants.ES_BQ_FLATTEN_STRUCT} to be true'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_OUTPUT_DATASET}',
            dest=constants.ES_BQ_OUTPUT_DATASET,
            required=True,
            help='BigQuery Output Dataset Name'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_OUTPUT_TABLE}',
            dest=constants.ES_BQ_OUTPUT_TABLE,
            required=True,
            help='BigQuery Output Table Name'
        )
        parser.add_argument(
            f'--{constants.ES_BQ_OUTPUT_MODE}',
            dest=constants.ES_BQ_OUTPUT_MODE,
            required=False,
            default=constants.OUTPUT_MODE_APPEND,
            help=(
                'BigQuery Output write mode '
                '(one of: append,overwrite,ignore,errorifexists) '
                '(Defaults to append)'
            ),
            choices=[
                constants.OUTPUT_MODE_OVERWRITE,
                constants.OUTPUT_MODE_APPEND,
                constants.OUTPUT_MODE_IGNORE,
                constants.OUTPUT_MODE_ERRORIFEXISTS
            ]
        )

        known_args: argparse.Namespace
        known_args, _ = parser.parse_known_args(args)

        return vars(known_args)

    def run(self, spark: SparkSession, args: Dict[str, Any]) -> None:

        logger: Logger = self.get_logger(spark=spark)

        # Arguments
        es_node: str = args[constants.ES_BQ_INPUT_NODE]
        es_index: str = args[constants.ES_BQ_INPUT_INDEX]
        es_user: str = args[constants.ES_BQ_NODE_USER]
        es_password: str = args[constants.ES_BQ_NODE_PASSWORD]
        flatten_struct = args[constants.ES_BQ_FLATTEN_STRUCT]
        flatten_array = args[constants.ES_BQ_FLATTEN_ARRAY]
        output_mode: str = args[constants.ES_BQ_OUTPUT_MODE]
        big_query_output_dataset: str = args[constants.ES_BQ_OUTPUT_DATASET]
        big_query_output_table: str = args[constants.ES_BQ_OUTPUT_TABLE]

        ignore_keys = {constants.ES_BQ_NODE_PASSWORD}
        filtered_args = {key:val for key,val in args.items() if key not in ignore_keys}
        logger.info(
            "Starting Elasticsearch to BigQuery Spark job with parameters:\n"
            f"{pprint.pformat(filtered_args)}"
        )

        # Read
        input_data = ingest_dataframe_from_elasticsearch(
            spark, es_node, es_index, es_user, es_password, args, "es.bq.input."
        )

        if flatten_struct:
            # Flatten the Struct Fields
            input_data = flatten_struct_fields(input_data)

            if flatten_array:
                # Flatten the n-D array fields to 1-D array fields
                input_data = flatten_array_fields(input_data)

        # Write
        input_data.write \
                .format(constants.FORMAT_BIGQUERY) \
                .option(constants.WRITE_METHOD, constants.DIRECT)\
                .option(constants.TABLE, big_query_output_dataset + "." + big_query_output_table) \
                .mode(output_mode) \
                .save()