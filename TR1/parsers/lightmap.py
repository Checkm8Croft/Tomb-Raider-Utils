def read_lightmap(f):
    """
    Reads fixed-size LightMap (32*256 bytes)
    """
    return len(f.read(32 * 256))
