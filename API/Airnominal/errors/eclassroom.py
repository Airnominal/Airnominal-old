from .base import AirnominalError


class ClassroomError(AirnominalError):
    pass


class ClassroomApiError(ClassroomError):
    pass


class InvalidTokenError(ClassroomApiError):
    pass


class InvalidRecordError(ClassroomApiError):
    pass


class LunchScheduleError(ClassroomError):
    pass
