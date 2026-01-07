import struct

# parsers/rooms.py

def read_rooms_safe(f):
    """
    Safe read: only reads NumRooms and does not read room data.
    This will return the correct number of rooms without crashing.
    """
    # Skip 4 bytes unused after textiles
    f.read(4)

    # NumRooms (2 bytes, little endian)
    num_rooms = int.from_bytes(f.read(2), byteorder="little")
    
    return num_rooms
