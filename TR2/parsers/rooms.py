def parse_rooms(reader):
    # NumRooms (2 byte)
    return reader.read_u16()
