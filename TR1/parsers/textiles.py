import struct

def read_textiles(f):
    """
    Reads number of textiles. Returns NumTextiles.
    """
    f.seek(4)  # after Version
    num_textiles = struct.unpack("<I", f.read(4))[0]
    return num_textiles
