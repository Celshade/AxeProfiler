class Profile():
    """
    """
    def __init__(self, data: dict[str, str]):
        self._data = data

    def __repr__(self):
        return f"Profile({self._data})"

    def __str__(self):
        return "hi profile"

