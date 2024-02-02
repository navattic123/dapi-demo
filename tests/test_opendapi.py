# pylint: disable=unnecessary-lambda-assignment
"""Test and auto-update opendapis"""
import os
from typing import Dict

from opendapi.utils import get_root_dir_fullpath
from opendapi.validators.runner import Runner

# In the demo app, we are importing the pynamodb base model. In real-world
# applications, you should import your own base model.
from pynamodb.models import Model


class TodosDapiRunner(Runner):
    """Demo App DAPI Runner"""

    REPO_ROOT_DIR_PATH = (
        get_root_dir_fullpath(__file__, "dapi-demo")
        if "dapi-demo-private" not in __file__
        else get_root_dir_fullpath(__file__, "dapi-demo-private")
    )
    DAPIS_DIR_PATH = os.path.join(REPO_ROOT_DIR_PATH, "dapis")

    ORG_NAME = "Todos"
    ORG_EMAIL_DOMAIN = "todos-inc.com"
    ORG_SLACK_TEAM = "T054K66G3J4"

    SEED_TEAMS_NAMES = ["Engineering"]
    SEED_DATASTORES_NAMES_WITH_TYPES = {
        "dynamodb": "dynamodb",
        "snowflake": "snowflake",
    }

    PYNAMODB_TABLES_BASE_CLS = Model
    PYNAMODB_PRODUCER_DATASTORE_NAME = "dynamodb"
    PYNAMODB_CONSUMER_SNOWFLAKE_DATASTORE_NAME = "snowflake"
    PYNAMODB_CONSUMER_SNOWFLAKE_IDENTIFIER_MAPPER = lambda self, table_name: (
        "todos.dynamodb",
        f"production_{table_name}",
    )

    ADDITIONAL_DAPI_VALIDATORS = []


def test_and_autoupdate_dapis():
    """Test and auto-update dapis"""
    runner = TodosDapiRunner()
    runner.run()
