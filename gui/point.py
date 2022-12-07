class Point:
    def __init__(self, x: float, y: float, z: float = None, color=None) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.color = color

    def __str__(self) -> str:
        if self.z is None:
            return str(self.x) + '-' + str(self.y)

        return str(self.x) + '-' + str(self.y) + '-' + str(self.z)
