# NASM-BrainF-Compiler
Compiles Brainf*** code into NASM assembly and links it to create an executable.

# Usage
The file is called `main.py` rn but you can change it or smth. The target file path **MUST** come after `main.py` (or whatever you named it).
```sh
python main.py path/to/code.bf
```
This will create a files in that path (the filenames are based on the original filename):
- `code.asm`
- `code.o`
- `code` (executable)

To run your brainf code, just `./code`

You can also pass `--detail` to `main.py` to add some comments to the assembly file.
```sh
python main.py path/to/code.bf --detail
```
