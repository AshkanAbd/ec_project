class Point:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = None) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return str(self.x) + '-' + str(self.y)
