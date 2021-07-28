from abc import abstractmethod


class Piece:
    def __init__(self, type, position, active, shape, flip, image, lens):
        self.type = type
        self.position = position
        self.active = active
        self.shape = shape
        self.flip = flip
        self.image = image
        self.lens = lens

    def moveDown(self):
        self.position[1] += 1

    def activeOff(self):
        self.active = False

    def getActive(self):
        return self.active

    def getPosition(self):
        return self.position

    def moveSide(self, dx):
        self.position[0] += dx

    def pieceMatrix(self):
        return self.shape

    @abstractmethod
    def yLenInd(self):
        pass

    @abstractmethod
    def xLenInd(self):
        pass

    @abstractmethod
    def rotation(self, dir):
        pass

    @abstractmethod
    def rotationImg(self, dir):
        pass

    @abstractmethod
    def getStart(self):
        pass


class I(Piece):
    def __init__(self):
        self.type = "I"
        self.position = [3, 1]
        self.active = True
        self.shape = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.flip = 0
        self.rots = [
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
        ]
        self.lens = [2, 4, 3, 4]
        self.start = [1, 3, 1, 2]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]


class O(Piece):
    def __init__(self):
        self.type = "O"
        self.position = [3, 0]
        self.active = True
        self.shape = [[1, 1], [1, 1]]
        self.flip = False

    def yLenInd(self, dir):
        return 2

    def xLenInd(self, dir):
        return 2

    def getStart(self, dir):
        return 1

    def rotation(self, dir):
        return self.shape

    def rotationImg(self, dir):
        return self.shape


class T(Piece):
    def __init__(self):
        self.type = "T"
        self.position = [3, 1]
        self.active = True
        self.shape = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
        self.flip = 0
        self.rots = [
            [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
            [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
            [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
            [[0, 1, 0], [1, 1, 0], [0, 1, 0]],
        ]
        self.lens = [2, 3, 3, 3]
        self.start = [1, 2, 1, 1]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]


class L(Piece):
    def __init__(self):
        self.type = "L"
        self.position = [3, 1]
        self.active = True
        self.shape = [[0, 1, 0], [0, 1, 0], [0, 1, 1]]
        self.flip = 0
        self.rots = [
            [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
            [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
            [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
        ]
        self.lens = [3, 3, 3, 2]
        self.start = [2, 1, 1, 1]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]


class J(Piece):
    def __init__(self):
        self.type = "L"
        self.position = [3, 1]
        self.active = True
        self.shape = [[0, 1, 0], [0, 1, 0], [1, 1, 0]]
        self.flip = 0
        self.rots = [
            [[0, 1, 0], [0, 1, 0], [1, 1, 0]],
            [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
            [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
            [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
        ]
        self.lens = [3, 2, 3, 3]
        self.start = [1, 1, 2, 1]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]


class S(Piece):
    def __init__(self):
        self.type = "S"
        self.position = [3, 1]
        self.active = True
        self.shape = [[0, 1, 1], [1, 1, 0], [0, 0, 0]]
        self.flip = 0
        self.rots = [
            [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
            [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
            [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
            [[1, 0, 0], [1, 1, 0], [0, 1, 0]],
        ]
        self.lens = [2, 3, 3, 3]
        self.start = [1, 2, 1, 1]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]


class Z(Piece):
    def __init__(self):
        self.type = "Z"
        self.position = [3, 1]
        self.active = True
        self.shape = [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
        self.flip = 0
        self.rots = [
            [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
            [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
            [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [1, 1, 0], [1, 0, 0]],
        ]
        self.lens = [2, 3, 3, 3]
        self.start = [1, 2, 1, 1]

    def yLenInd(self, dir):
        return self.lens[(self.flip + dir) % 4]

    def xLenInd(self, dir):
        return self.lens[(self.flip + dir + 1) % 4]

    def getStart(self, dir):
        return self.start[(self.flip + dir) % 4]

    def rotation(self, dir):
        self.flip = (self.flip + dir) % 4
        self.shape = self.rots[self.flip]

    def rotationImg(self, dir):
        return self.rots[(self.flip + dir) % 4]
