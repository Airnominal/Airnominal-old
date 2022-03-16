from .base import AirnominalError


class MenuError(AirnominalError):
    pass


class MenuApiError(MenuError):
    pass


class MenuDateError(MenuError):
    pass


class MenuFormatError(MenuError):
    pass
