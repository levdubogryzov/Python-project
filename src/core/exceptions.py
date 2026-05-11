class AlgorithmError(Exception):
    """Базовое исключение для ошибок алгоритмов."""
    pass


class EventProtocolError(AlgorithmError):
    """Ошибка протокола событий."""
    pass


class ValidationError(AlgorithmError):
    """Ошибка валидации данных или результатов."""
    pass


class InvalidInputError(AlgorithmError):
    """Ошибка некорректных входных данных."""
    pass


class NegativeCycleError(AlgorithmError):
    """Ошибка обнаружения отрицательного цикла в графе."""
    pass


class ReplayError(AlgorithmError):
    """Ошибка воспроизведения сценария."""
    pass
