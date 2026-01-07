import struct

def u16(f):
    return struct.unpack("<H", f.read(2))[0]

def u32(f):
    return struct.unpack("<I", f.read(4))[0]

def parse_header(f):
    """
    Reads the main header of a TR1 level:
    - Version
    - Number of Textiles
    - Number of Rooms
    """
    f.seek(0)
    version = u32(f)
    num_textiles = u32(f)
    
    # Skip the actual 8-bit textures (each 64kB)
    f.seek(num_textiles * 65536, 1)
    
    unused = u32(f)
    num_rooms = u16(f)

    return {
        "version": version,
        "num_textiles": num_textiles,
        "num_rooms": num_rooms
    }
