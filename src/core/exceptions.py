class AlgorithmError(Exception):
    """Базовое исключение алгоритмов."""
    pass


class InvalidInputError(AlgorithmError):
    """Ошибка некорректных входных данных."""
    pass


class EventProtocolError(AlgorithmError):
    """Ошибка нарушения протокола событий."""
    pass
