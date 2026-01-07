# TR1 Level Inspector (Python)

This is a simple Python tool to inspect Tomb Raider 1 `.PHD` level files.  

> ⚠️ **Note:** This tool only reads the values that can be safely extracted without crashing. Many parts of the `.PHD` file (like objects, triggers, meshes, animations, etc.) are **not parsed** and will always show `0` or are omitted.

---

## Features

The script currently reads:

- **Version** – Level file version.
- **Textiles** – Number of textures in the level.
- **Rooms** – Number of rooms in the level (**safe** reading).
- **LightMap** – Total bytes in the light map (optional, fixed size: 8192 bytes).
- **Palette** – Number of colors in the palette (optional, 256 colors).
- **SoundMap** – Number of sound entries (optional, 256 entries).

The **rooms count** uses a "safe" reading method to avoid crashing or returning incorrect numbers.

---

## Usage

```bash
python3 phd_reader.py <path_to_phd_file>
