import sys
from parsers.binary_reader import BinaryReader
from parsers.textures import parse_textures
from parsers.rooms import parse_rooms
from parsers.floor_data import parse_floor_data

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 level_reader.py <path al file .tr2>")
        return

    level_path = sys.argv[1]

    with open(level_path, "rb") as f:
        reader = BinaryReader(f)

        # Version
        version = reader.read_u32()
        print(f"Version: {hex(version)}")

        # --- SALTO PALETTE PRIMA DI LEGGERE NUMTEXTILES ---
        reader.skip(256*3)  # Palette 8-bit
        reader.skip(256*4)  # Palette 16-bit

        # Textures
        num_textures = parse_textures(reader)
        print(f"Num textures: {num_textures}")

        # Rooms
        num_rooms = parse_rooms(reader)
        print(f"Num rooms: {num_rooms}")

        # Floor data
        num_floor_data = parse_floor_data(reader)
        print(f"Floor data entries: {num_floor_data}")

if __name__ == "__main__":
    main()
