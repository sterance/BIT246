import os
from pathlib import Path

script_dir = Path(__file__).resolve().parent

file_path = script_dir / "example.jpg"
output_path = script_dir / "output.jpg"
with open(file_path, "rb") as file:
    binary_data = file.read()

with open(output_path, "wb") as file:
    file.write(binary_data)

original_size = os.path.getsize(file_path)
output_size = os.path.getsize(output_path)

if original_size == output_size:
    print(f"Both files are {original_size} bytes.")
else:
    raise ValueError(f"Original is {original_size} bytes, output is {output_size} bytes.")