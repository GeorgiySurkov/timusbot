class CommandParseError(Exception):
    pass


class TrackCommandParseError(CommandParseError):
    pass


class UntrackCommandParseError(CommandParseError):
    pass


class UserNotFound(Exception):
    pass