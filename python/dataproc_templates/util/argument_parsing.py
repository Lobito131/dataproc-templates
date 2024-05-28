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

from typing import Optional, Sequence, Union
import argparse

import dataproc_templates.util.template_constants as constants
from dataproc_templates import TemplateName


def get_template_name(args: Optional[Sequence[str]] = None) -> TemplateName:
    """
    Parses the template name option from the program arguments.

    This will print the command help and exit if the --template
    argument is missing.

    Args:
        args (Optional[Sequence[str]]): The program arguments.
            By default, command line arguments will be used.

    Returns:
        str: The value of the --template argument
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        add_help=False
    )

    parser.add_argument(
        '--template',
        dest='template_name',
        type=str,
        required=False,
        default=None,
        choices=TemplateName.choices(),
        help='The name of the template to run'
    )

    known_args: argparse.Namespace
    known_args, _ = parser.parse_known_args(args=args)

    if known_args.template_name is None:
        parser.print_help()
        parser.exit()

    return TemplateName.from_string(known_args.template_name)


def get_log_level(args: Optional[Sequence[str]] = None) -> str:
    """
    Parses the log level option from the program arguments.

    INFO is the default log level
    This will exit if the log level in an invalid choice.

    Args:
        args (Optional[Sequence[str]]): The program arguments.
            By default, command line arguments will be used.

    Returns:
        str: The value of the --log_level argument
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        add_help=False
    )

    parser.add_argument(
        '--log_level',
        dest='log_level',
        type=str,
        required=False,
        default="INFO",
        choices=["ALL", "DEBUG", "ERROR", "FATAL", "INFO", "OFF", "TRACE", "WARN"],
        help='Spark Context Log Level'
    )

    known_args: argparse.Namespace
    known_args, _ = parser.parse_known_args(args=args)

    return known_args.log_level


def add_spark_options(parser: argparse.ArgumentParser, template_to_spark_option_map: dict, read_options: bool = True) -> None:
    if not template_to_spark_option_map:
        return

    for option_name, spark_option_name in template_to_spark_option_map.items():
        if read_options:
            help_text = (constants.SPARK_OPTIONS[spark_option_name].get(constants.OPTION_READ_HELP, "")
                         or constants.SPARK_OPTIONS[spark_option_name].get(constants.OPTION_HELP, ""))
        else:
            help_text = (constants.SPARK_OPTIONS[spark_option_name].get(constants.OPTION_WRITE_HELP, "")
                         or constants.SPARK_OPTIONS[spark_option_name].get(constants.OPTION_HELP, ""))
        parser.add_argument(
            f'--{option_name}',
            dest=option_name,
            required=False,
            default=constants.SPARK_OPTIONS[spark_option_name].get(constants.OPTION_DEFAULT, ""),
            help=help_text
        )

def add_es_spark_connector_options(parser: argparse.ArgumentParser, template_to_es_spark_reader_option_map: dict) -> None:
    if not template_to_es_spark_reader_option_map:
        return

    for option_name, es_spark_reader_option_name in template_to_es_spark_reader_option_map.items():
        help_text = (constants.ES_SPARK_READER_OPTIONS[es_spark_reader_option_name].get(constants.OPTION_HELP, ""))

        parser.add_argument(
            f'--{option_name}',
            dest=option_name,
            required=False,
            default=constants.ES_SPARK_READER_OPTIONS[es_spark_reader_option_name].get(constants.OPTION_DEFAULT, ""),
            help=help_text
        )