from marshmallow.exceptions import MarshmallowError


class ValidationConflictError(MarshmallowError):
    def __init__(self, message):
        self.messages = message
    pass
