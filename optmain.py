"""
My go at optimizing the assembly code.
this time it seriously might not work on all machines.

so optimizing means trying out FASM? okay then.

Taking inspiration from Porth by Tsoding
Latest (go check it out!): https://gitlab.com/tsoding/porth/
I'm looking through: https://github.com/tsoding/porth/blob/a6ddbe8f65c3a155932ca34217ceccee6b88b931/porth.py

Also thank you to the countless assembly websites I've read.

I will format this mess into something readable soon™

Notes:
the memory size is 1024 cells. you can increase (or decrease) it below where it says
"%define MEMORY_SIZE 1024"
"""

import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("No file supplied.")
        sys.exit(1)

    with open(sys.argv[1]) as file:
        code = list(filter(lambda c: c in "+-.,><[]", file.read()))

    base = sys.argv[1].split(".")[0]
    program = generate_fasm_linux_x86_64(code)

    with open(base + ".asm", "w+") as f:
        f.write(program)
    print(f"fasm {base}.asm")
    subprocess.Popen(["fasm", base + ".asm"])
    
    

def generate_fasm_linux_x86_64(code: str) -> str:
    asm = """\
format ELF64 executable
entry _start

segment readable writeable
    memory     times MEMORY_SIZE db 0

section '.text' readable executable
_start:{}
    mov     rax, 0""".format("\n    ;; initialize pointer" if "--detail" in sys.argv else "")

    index = 0
    loop_stack = []
    total_loops = 0

    while index < len(code):
        char = code[index]
        count = 1
        
        # Optimize repetitive operations
        if char in "+-" or char in "><":
            char_set = "+-" if char in "+-" else "><"
            while index < len(code) and code[index + 1] in char_set:
                count += 1 if code[index + 1] == char else -1
                index += 1
        
        # Add comments to the assembly
        if "--detail" in sys.argv:
            asm += f"\n    ;; {char}"
        
        if char == "+":
            asm += f"\n    add     BYTE [memory + rax], {count}"
        
        elif char == "-":
            asm += f"\n    sub     BYTE [memory + rax], {count}"
        
        elif char == ">":
            asm += f"\n    add     rax, {count}"
            
        elif char == "<":
            asm += f"\n    sub     rax, {count}"
            
        elif char == ".":
            asm += """
    mov     edx, 1
    mov     esi, 48
    mov     edi, 1
    push    rax
    mov     rax, 1
    syscall
    pop     rax"""
            
        elif char == ",":
            asm += """
    call    readch
    mov     BYTE [memory + rax], eax"""

        elif char == "[":
            total_loops += 1
            asm += f"""
open_{total_loops}:
    cmp     BYTE [memory + rax], 0
    je      close_{total_loops}"""
            loop_stack.append(total_loops)

        elif char == "]":
            label = loop_stack.pop()
            asm += f"""
    jmp     open_{label}
close_{label}:"""

        index += 1

    # Add comments to the assembly
    if "--detail" in sys.argv:
        asm += "\n    ;; exit program"
    asm += """
    mov     rax, 60
    mov     rdi, 0
    syscall
"""

    # Functions
    asm += """
putch:
    sub     rsp, 24
    mov     edx, 1
    mov     BYTE [rsp+12], dil
    lea     rsi, [rsp+12]
    mov     edi, 1
    mov     rax, 1
    syscall
    add     rsp, 24
ret""" if "." in code else ""

    asm += """
readch:
    sub     rsp, 24
    mov     edx, 1
    mov     edi, 1
    lea     rsi, [rsp+15]
    mov     rax, 0
    syscall
    movzx   eax, BYTE [rsp+15]
    add     rsp, 24
ret""" if "," in code else ""

    return asm

if __name__ == "__main__":
    main()
