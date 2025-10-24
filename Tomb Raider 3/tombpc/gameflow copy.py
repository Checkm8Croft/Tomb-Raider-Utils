import sys
import struct

def read_uint16(f):
    return struct.unpack("<H", f.read(2))[0]

def read_uint32(f):
    return struct.unpack("<I", f.read(4))[0]

def read_bytes(f, n):
    return f.read(n)

def read_string_table(f, count, xor):
    strings = []
    if count == 0:
        f.read(2)
        return strings

    offsets = [read_uint16(f) for _ in range(count + 1)]

    for i in range(count):
        length = offsets[i + 1] - offsets[i] - 1
        data = bytes([f.read(1)[0] ^ xor for _ in range(length)])
        strings.append(data.decode("latin1"))  # non ASCII, latin1 sicuro
        f.read(1)  # xor padding
    return strings

def main(filename):
    with open(filename, "rb") as f:
        version = read_uint32(f)
        description = f.read(256).split(b'\0')[0].decode("latin1")
        gameflow_size = read_uint16(f)
        first_option = read_uint32(f)
        title_replace = struct.unpack("<i", f.read(4))[0]
        death_demo = read_uint32(f)
        death_ingame = read_uint32(f)
        demo_time = read_uint32(f)
        demo_interrupt = read_uint32(f)
        demo_end = read_uint32(f)
        f.read(36)  # padding1

        num_levels = read_uint16(f)
        num_pictures = read_uint16(f)
        num_titles = read_uint16(f)
        num_rpls = read_uint16(f)
        num_cutscenes = read_uint16(f)
        num_demo_levels = read_uint16(f)
        f.read(2)  # title sound
        f.read(2)  # single level
        f.read(32)  # padding2

        f.read(2)  # flags
        f.read(6)  # padding3

        xor = f.read(1)[0]
        f.read(1)  # language
        f.read(1)  # secret sound
        f.read(5)  # padding4

        level_names = read_string_table(f, num_levels, xor)
        picture_names = read_string_table(f, num_pictures, xor)
        title_file_names = read_string_table(f, num_titles, xor)
        rpl_file_names = read_string_table(f, num_rpls, xor)
        level_file_names = read_string_table(f, num_levels, xor)
        cutscene_file_names = read_string_table(f, num_cutscenes, xor)

    print("Levels:", level_names)
    print("Level files:", level_file_names)
    print("Pictures:", picture_names)
    print("Titles:", title_file_names)
    print("RPLs:", rpl_file_names)
    print("Cutscenes:", cutscene_file_names)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gameflow.py <TOMBPC.DAT>")
        sys.exit(1)
    main(sys.argv[1])
