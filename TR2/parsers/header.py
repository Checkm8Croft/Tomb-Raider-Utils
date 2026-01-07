def parse_header(reader):
    version = reader.read_u32()

    # Palette 8-bit: 256 RGB triplets
    reader.skip(256 * 3)

    # Palette 16-bit: 256 RGBA (or ARGB)
    reader.skip(256 * 4)

    return version
