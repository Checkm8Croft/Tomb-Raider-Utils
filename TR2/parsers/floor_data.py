def parse_floor_data(reader):
    # Num floor data entries (2 byte)
    return reader.read_u16()
