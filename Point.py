import numpy as np

class Point:
    def __init__(self, pos, ID):
        """
        import numpy as np
            pos = list of 3 integers [x,y,z]
            ID = string label
        """
        self.pos = pos
        self.ID = ID

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if type(value) != list or not all(isinstance(item, float) for item in value):
            raise TypeError("Incorrect position type")
        self._pos = np.array(value)

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        if type(value) != str:
            raise TypeError("The ID isn't a string")
        self._ID = value

    def getDistance(self, p2):
        return np.linalg.norm(self.pos-p2.pos)

    def isNull(self):
        if self.pos[0]==0 and self.pos[1] == 0 and self.pos[2]==0:
            return True
        return False

    def __str__(self):
        return """
        POINT ID : {}

        x - {}
        y - {}
        z - {}""".format(self.ID, self.pos[0], self.pos[1], self.pos[2])
