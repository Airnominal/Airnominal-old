import os
import sys

import click
from flask.cli import FlaskGroup, ScriptInfo

from .errors import ConfigError


class AirNominalGroup(FlaskGroup):
    """
    Special subclass of the :class:`~flask.cli.FlaskGroup` group that
    supports setting configuration file as a command argument and modifies
    the help text.
    """

    def __init__(self):
        def _set_config_filename(ctx, param, value):
            """Set configuration file from argument."""

            if value:
                os.environ["AIRNOMINAL_CONFIG"] = value

        def _get_version(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return

            import pkg_resources
            import platform

            python_version = platform.python_version()
            airnominal_version = pkg_resources.get_distribution("Airnominal").version
            sqlalchemy_version = pkg_resources.get_distribution("sqlalchemy").version
            requests_version = pkg_resources.get_distribution("requests").version
            flask_version = pkg_resources.get_distribution("flask").version

            click.echo(
                f"Python: {python_version}\n"
                f"AirNominal: {airnominal_version}\n"
                f"SQLAlchemy: {sqlalchemy_version}\n"
                f"Requests: {requests_version}\n"
                f"Flask: {flask_version}\n"

            )
            ctx.exit()

        params = [
            click.Option(
                ["--config"],
                help="Set a config file name.",
                metavar="filename",
                type=str,
                callback=_set_config_filename,
            ),
            click.Option(
                ["--version"],
                help="Show the AirNominal version and exit.",
                expose_value=False,
                callback=_get_version,
                is_flag=True,
                is_eager=True,
            ),
        ]

        help = (
            "A utility script for the AirNominal application.\n\n"
            "Configuration file can be provided as --config argument or as the "
            "AIRNOMINAL_CONFIG environment variable. Development mode can be "
            "enabled with the FLASK_ENV environment variable to 'development'.\n\n"
            "Note: Due to the limitations of the command parser, some application-specific "
            "commands won't be displayed in the command list if the configuration file "
            "is not specified as environment variable or is invalid."
        )

        # Use custom version option to display arguments in correct order and add other relevant versions
        super().__init__(add_version_option=False, params=params, help=help)

    def main(self, as_module=False):
        """Set a Flask app and start the main command handler."""

        os.environ["FLASK_APP"] = "Airnominal"
        super().main(args=sys.argv[1:], prog_name="python -m Airnominal" if as_module else None)


def main(as_module=False):
    def _list_commands(self, ctx):
        self._load_plugin_commands()

        rv = set(super(FlaskGroup, self).list_commands(ctx))
        info = ctx.ensure_object(ScriptInfo)
        os.environ["AIRNOMINAL_CONFIG"] = "config.yaml"
        try:
            rv.update(info.load_app().cli.list_commands(ctx))
        except ConfigError as error:
            click.secho(f"Error: {error}", err=True, fg="red")

        return sorted(rv)

    # Monkey-patch Flask's list_commands to hide any config errors when showing list of commands or help
    FlaskGroup.list_commands = _list_commands

    # Run AirNominal's command group
    cli = AirNominalGroup()
    cli.main(as_module)


if __name__ == "__main__":
    main(as_module=True)