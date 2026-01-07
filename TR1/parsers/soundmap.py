import struct

def read_soundmap(f):
    """
    Reads fixed-size SoundMap (256 int16_t)
    """
    return list(struct.unpack("<256h", f.read(512)))
