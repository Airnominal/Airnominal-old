import datetime
import logging

import click
from flask import current_app
from flask.cli import with_appcontext

from ..database import Base
from sqlalchemy import create_engine, or_
from ..utils import session_scope, with_transaction


@click.command("create-database", help="Create the database.")
@with_transaction(name="create-database", op="command")
@with_appcontext
def create_database_command():
    """Create a new database and all tables."""
    logging.getLogger(__name__).info("Creating the database")
    engine = create_engine(self.config["database"])
    Base.metadata.create_all(current_app.airnominal.engine)
