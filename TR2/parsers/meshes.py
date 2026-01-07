def parse_meshes(reader):
    num_mesh_data = reader.read_u32()
    reader.skip(num_mesh_data * 2)  # int16_t mesh data

    num_mesh_pointers = reader.read_u32()
    reader.skip(num_mesh_pointers * 4)  # uint32_t offsets
