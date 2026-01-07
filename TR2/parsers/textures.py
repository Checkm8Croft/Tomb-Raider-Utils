def parse_textures(reader):
    # NumTextiles
    num_textiles = reader.read_u32()

    # Skip textile data
    reader.skip(num_textiles * 65536)    # Textile8
    reader.skip(num_textiles * 131072)   # Textile16

    # Skip unused 4 bytes
    reader.skip(4)

    return num_textiles
