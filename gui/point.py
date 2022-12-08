class Point:
    def __init__(self, x, y: float = None, z: float = None, color=None) -> None:
        self.y = None
        self.z = None
        if type(x) is list:
            dimension = len(x)
            if dimension >= 1:
                self.x = x[0]
            if dimension >= 2:
                self.y = x[1]
            if dimension >= 3:
                self.z = x[2]
        elif type(x) is int or type(x) is float:
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
