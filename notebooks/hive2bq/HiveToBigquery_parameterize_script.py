# Copyright 2023 Google LLC
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

from os import environ
from typing import Dict, Sequence, Optional, Any
import argparse

import papermill as pm

from parameterize_script import BaseParameterizeScript
import parameterize_script.util.notebook_constants as constants

__all__ = ['HiveToBigQueryScript']


class HiveToBigQueryScript(BaseParameterizeScript):

    """
    Script to parameterize HiveToBigQuery notebook.
    """

    @staticmethod
    def parse_args(args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            f'--{constants.OUTPUT_NOTEBOOK_ARG}',
            dest=constants.OUTPUT_NOTEBOOK_ARG,
            required=False,
            default=None,
            help='Path to save executed notebook (Default: None). '
            'If not provided, no notebook is saved'
        )

        parser.add_argument(
            f'--{constants.HIVE_METASTORE_ARG}',
            dest=constants.HIVE_METASTORE,
            required=True,
            help='Hive metastore URI'
        )

        parser.add_argument(
            f'--{constants.INPUT_HIVE_DATABASE_ARG}',
            dest=constants.INPUT_HIVE_DATABASE,
            required=True,
            help='Hive database name'
        )

        parser.add_argument(
            f'--{constants.INPUT_HIVE_TABLES_ARG}',
            dest=constants.INPUT_HIVE_TABLES,
            required=False,
            default="*",
            help='Comma separated list of Hive tables to be migrated "/table1,table2,.../" (Default: *)'
        )

        parser.add_argument(
            f'--{constants.OUTPUT_BIGQUERY_DATASET_ARG}',
            dest=constants.OUTPUT_BIGQUERY_DATASET,
            required=True,
            help='BigQuery dataset name'
        )

        parser.add_argument(
            f'--{constants.TEMP_BUCKET_ARG}',
            dest=constants.TEMP_BUCKET,
            required=True,
            help='GCS bucket name for temporary staging'
        )

        parser.add_argument(
            f'--{constants.HIVE_OUTPUT_MODE_ARG}',
            dest=constants.HIVE_OUTPUT_MODE,
            required=False,
            default=constants.OUTPUT_MODE_OVERWRITE,
            help='Hive output mode (Default: overwrite)',
            choices=[constants.OUTPUT_MODE_OVERWRITE,
                     constants.OUTPUT_MODE_APPEND]
        )

        parser.add_argument(
            f'--{constants.MAX_PARALLELISM_ARG}',
            dest=constants.MAX_PARALLELISM,
            type=int,
            default=5,
            required=False,
            help='Maximum number of tables that will migrated parallelly (Default: 5)'
        )

        known_args: argparse.Namespace
        known_args, _ = parser.parse_known_args()

        return vars(known_args)

    def get_env_var(self, parameters) -> Dict[str, Any]:
        """
        Get the environment variables.
        """
        parameters[constants.PROJECT] = environ[constants.GCP_PROJECT]
        parameters[constants.REGION] = environ[constants.REGION]
        parameters[constants.GCS_STAGING_LOCATION] = environ[constants.GCS_STAGING_LOCATION]
        parameters[constants.SUBNET] = environ[constants.SUBNET] if constants.SUBNET in environ else ""
        parameters[constants.IS_PARAMETERIZED] = True

        return parameters

    def run(self, args: Dict[str, Any]) -> None:
        """
        Run the notebook.
        """

        # Exclude arguments that are not needed to be passed to the notebook
        ignore_keys = {constants.OUTPUT_NOTEBOOK_ARG}
        nb_parameters = {key:val for key,val in args.items() if key not in ignore_keys}

        # Get environment variables
        nb_parameters = self.get_env_var(nb_parameters)

        # Run the notebook
        output_path = args[constants.OUTPUT_NOTEBOOK_ARG]
        pm.execute_notebook(
            'hive2bq/HiveToBigquery_notebook.ipynb',
            output_path,
            nb_parameters
        )