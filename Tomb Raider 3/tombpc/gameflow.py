import sys
import struct

def read_uint16(f):
    data = f.read(2)
    if len(data) < 2:
        raise EOFError("Tentativo di leggere uint16 oltre la fine del file")
    return struct.unpack("<H", data)[0]

def read_uint32(f):
    data = f.read(4)
    if len(data) < 4:
        raise EOFError("Tentativo di leggere uint32 oltre la fine del file")
    return struct.unpack("<I", data)[0]

def read_string_table(f, count, xor, label=""):
    strings = []
    print(f"--- Lettura stringhe {label}, count = {count} ---")
    if count == 0:
        f.read(2)  # skip padding
        print(f"{label}: zero elementi, skip 2 byte padding")
        return strings

    offsets = []
    for i in range(count + 1):
        try:
            offset = read_uint16(f)
            offsets.append(offset)
        except EOFError:
            print(f"EOF raggiunto leggendo offset {i} di {label}")
            break

    print(f"{label} offsets: {offsets}")

    for i in range(count):
        if i + 1 >= len(offsets):
            print(f"Warning: indice offset fuori range per {label}")
            break
        length = offsets[i + 1] - offsets[i] - 1
        if length < 0:
            length = 0
        data_bytes = f.read(length)
        if len(data_bytes) < length:
            print(f"Warning: letti {len(data_bytes)} byte su {length} previsti per {label}[{i}]")
        data = bytes([b ^ xor for b in data_bytes])
        strings.append(data.decode("latin1"))
        f.read(1)  # xor padding
    print(f"{label} letti: {strings}")
    return strings

def clean_gamestrings(strings):
    cleaned = []
    for s in strings:
        # Mantieni solo caratteri leggibili (ASCII e alfabetici estesi)
        s_clean = ''.join(c if (32 <= ord(c) <= 126 or (ord(c) > 127 and c.isalpha())) else '' for c in s)
        if not s_clean:
            s_clean = ' '  # sostituisci stringhe vuote o solo alieno con spazio
        cleaned.append(s_clean)
    return cleaned

def main(filename):
    with open(filename, "rb") as f:
        version = read_uint32(f)
        description = f.read(256).split(b'\0')[0].decode("latin1")
        print(f"Version: {version}, Description: {description}")

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
        print(f"XOR value: {xor}")
        f.read(1)  # language
        f.read(1)  # secret sound
        f.read(5)  # padding4

        # Lettura stringhe principali
        level_names = read_string_table(f, num_levels, xor, "Levels")
        picture_names = read_string_table(f, num_pictures, xor, "Pictures")
        title_file_names = read_string_table(f, num_titles, xor, "Titles")
        rpl_file_names = read_string_table(f, num_rpls, xor, "RPLs")
        level_file_names = read_string_table(f, num_levels, xor, "Level Files")
        cutscene_file_names = read_string_table(f, num_cutscenes, xor, "Cutscenes")

        # GameStrings1
        try:
            num_game_strings1 = read_uint16(f)
            print(f"NumGameStrings1: {num_game_strings1}")
            game_strings1 = read_string_table(f, num_game_strings1, xor, "GameStrings1")
        except EOFError:
            print("EOF raggiunto prima di leggere GameStrings1")
            game_strings1 = []

        # GameStrings2 (41 stringhe come da C#)
        num_game_strings2 = 41
        game_strings2 = read_string_table(f, num_game_strings2, xor, "GameStrings2")
        game_strings2 = clean_gamestrings(game_strings2)

    print("\n=== Risultato finale ===")
    print("Levels:", level_names)
    print("Level files:", level_file_names)
    print("Pictures:", picture_names)
    print("Titles:", title_file_names)
    print("RPLs:", rpl_file_names)
    print("Cutscenes:", cutscene_file_names)
    print("GameStrings1:", game_strings1)
    print("GameStrings2:", game_strings2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gameflow.py <TOMBPC.DAT>")
        sys.exit(1)
    main(sys.argv[1])
