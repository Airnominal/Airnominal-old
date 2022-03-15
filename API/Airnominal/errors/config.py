from schema import SchemaError
from yaml import YAMLError

from .base import AirnominalError


class ConfigError(AirnominalError):
    pass


class ConfigReadError(ConfigError, OSError):
    pass


class ConfigParseError(ConfigError, YAMLError):
    pass


class ConfigValidationError(ConfigError, SchemaError):
    pass
