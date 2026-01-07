import struct

def read_palette(f):
    """
    Reads fixed-size Palette (256 colors, RGB 3 bytes each)
    Returns list of tuples (r, g, b)
    """
    palette = [struct.unpack("BBB", f.read(3)) for _ in range(256)]
    return palette
