from .platforms import PlatformsHandler
from sqlalchemy.orm import scoped_session
from .database import Session, Base
from flask import Flask, jsonify, render_template, request
import yaml
from schema import Optional, Or, Schema, SchemaError
from sqlalchemy import create_engine, or_
from .errors import ConfigError, ConfigParseError, ConfigReadError, ConfigValidationError
import os
from .commands import (
    create_database_command,
)
from werkzeug.exceptions import HTTPException
from .display import DisplayHandler
class Airnominal:
    schema = Schema(
        {
            "database": str,
            Optional("logging"): Or(dict, str)
        }
    )
    def __init__(self, configfile):
        try:
            with open(configfile, encoding="utf-8") as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        except OSError as error:
            raise ConfigReadError(str(error)) from error
        except yaml.YAMLError as error:
            raise ConfigParseError(str(error)) from error
        try:
            self.config = self.schema.validate(config)
        except SchemaError as error:
            raise ConfigValidationError(str(error)) from error
        

        self.session: scoped_session = None  # type: ignore
        self.engine = create_engine(self.config["database"])
        Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.app = Flask("Airnominal", static_folder=None)
        self.app.airnominal = self
        
        self.create_error_hooks()
        self.create_database_hooks()
        self.register_commands()
        self.registerHandlers()
        print(self.session)

    def configure_logging(self):
        """Configure logging from file or dict config if requested in the configuration file."""

        if "logging" in self.config:
            import logging.config

            if isinstance(self.config["logging"], dict):
                logging.config.dictConfig(self.config["logging"])
            elif isinstance(self.config["logging"], str):
                logging.config.fileConfig(self.config["logging"])
    def registerHandlers(self):
        # registracija /platforms/ routs
        self.platformsHandler = PlatformsHandler()
        self.app.register_blueprint(self.platformsHandler.reg, url_prefix="/platforms")
        self.displayHandler = DisplayHandler()
        self.app.register_blueprint(self.displayHandler.reg)
        print(self.app.url_map)
    
    
    def register_commands(self):
        """Register all application commands."""
        self.app.cli.add_command(create_database_command)
    
    def create_database_hooks(self):
        """Create and close the database session for each request."""

        @self.app.before_request
        def _create_session():
            self.session = scoped_session(Session)

        @self.app.teardown_request
        def _close_session(error):
            if error:
                self.session.rollback()
            else:
                self.session.commit()
                self.session.close()
    
    def create_error_hooks(self):
        """Add error handlers that will show errors as JSON."""

        @self.app.errorhandler(HTTPException)
        def resource_not_found(error):
            return (
                jsonify(
                    {
                        "error": {
                            "status": error.code,
                            "name": error.name,
                            "description": error.description,
                        },
                    },
                ),
                error.code,
            )
def create_app():
    """Application factory that accepts a configuration file from environment variable."""

    if "AIRNOMINAL_CONFIG" in os.environ:
        configfile = os.environ.get("AIRNOMINAL_CONFIG")
    else:
        raise ConfigError("Missing config filename")

    airnominal = Airnominal(configfile)
    return airnominal.app