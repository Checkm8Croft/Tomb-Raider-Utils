# phd_reader.py

import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 phd_reader.py <path_to_phd_file>")
        return

    path = sys.argv[1]

    with open(path, "rb") as f:
        # Version
        version = int.from_bytes(f.read(4), byteorder="little")
        print(f"Version:           {version}")

        # NumTextiles
        num_textiles = int.from_bytes(f.read(4), byteorder="little")
        print(f"Textiles:          {num_textiles}")

        # Skip actual textiles (safe)
        f.read(num_textiles * 65536)

        # Unused 4 bytes
        f.read(4)

        # NumRooms (safe)
        num_rooms = int.from_bytes(f.read(2), byteorder="little")
        print(f"Rooms:             {num_rooms}")

if __name__ == "__main__":
    main()
