class Point:
    def __init__(self, x: float, y: float = None, z: float = None, color=None) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.color = color

    def __str__(self) -> str:
        res = str(self.x)

        if self.y is not None:
            res += '-' + str(self.y)

        if self.z is not None:
            res += '-' + str(self.z)

        return res
