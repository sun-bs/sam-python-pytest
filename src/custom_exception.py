class CustomException(Exception):
    """
    メインロジックでキャッチさせる例外。
    """
    pass


class UncatchedException(Exception):
    pass
    """
    メインロジックでキャッチさせない例外。
    """