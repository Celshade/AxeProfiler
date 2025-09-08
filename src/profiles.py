class Profile():
    """
    """
    def __init__(self, data: dict[str, str]):
        self._data = data

    def __repr__(self):
        return f"__repr__ ->>\n Profile({self._data})"  # TODO remove __repr__ text

    def __str__(self):
        return "This is a profile printed from str()\n"

