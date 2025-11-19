import json
import sys
from pathlib import Path
from typing import TextIO

def read_mapping(path: Path) -> dict[str, str]:
    with path.open() as f:
        return json.load(f)

def substitute_objects(
    mapping: dict[str, str],
    input_file: TextIO,
    output_file: TextIO,
) -> None:
    for line in input_file:
        components = line.split()
        if components[0] != "o":
            output_file.write(line)
            continue

        object_name = components[1]
        mapped_name = mapping.get(object_name)
        if mapped_name:
            print(f"{object_name} -> {mapped_name}")
            object_name = mapped_name
        else:
            print("{object_name} not found, leaving as is")

        output_file.write(f"o {object_name}\n")



def main(args: list[str]) -> int:
    if len(args) < 4:
        print("Usage: [mapping.json] [input.obj] [output.obj]")
        return -1

    mapping_path = Path(sys.argv[1])
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    mapping = read_mapping(mapping_path)
    print(f"Loaded {len(mapping)} object mappings")

    with input_path.open() as input_file, output_path.open("w") as output_file:
        substitute_objects(mapping, input_file, output_file)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
