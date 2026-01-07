import struct

class BinaryReader:
    def __init__(self, f):
        self.f = f

    def read_u8(self):
        return struct.unpack("<B", self.f.read(1))[0]

    def read_u16(self):
        return struct.unpack("<H", self.f.read(2))[0]

    def read_u32(self):
        return struct.unpack("<I", self.f.read(4))[0]

    def skip(self, n):
        self.f.seek(n, 1)  # spostati n byte dalla posizione corrente
