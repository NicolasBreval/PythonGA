
class WrongInputTypeError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class HistoricalImportFormatError():
    def __init__(self, message) -> None:
        super().__init__(message)