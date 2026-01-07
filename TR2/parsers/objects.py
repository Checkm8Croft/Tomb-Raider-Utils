def parse_objects(reader):
    num_moveables = reader.read_u32()
    reader.skip(num_moveables * 32)  # struttura moveable TR2

    num_statics = reader.read_u32()
    reader.skip(num_statics * 32)  # struttura static TR2

    return num_moveables, num_statics
