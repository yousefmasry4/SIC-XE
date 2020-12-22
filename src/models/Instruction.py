
class instruction:
    def __init__(self, opcode, fmt):
        self.opcode = opcode << ((fmt - 1) * 8)
        self.inf = fmt

    def __str__(self):
        return f"{bin(self.opcode)}  :   {self.inf}"


PRELOAD_SYMTAB = {
    "A" : 0,
    "X" : 1,
    "B" : 4,
    "S" : 5,
    "T" : 6,
    "F" : 7,
}

OPTAB = {
    "ADD"    : instruction(0x18, 3),
    "ADDF"   : instruction(0x58, 3),
    "ADDR"   : instruction(0x90, 2),
    "AND"    : instruction(0x40, 3),
    "CLEAR"  : instruction(0xB4, 2),
    "COMP"   : instruction(0x28, 3),
    "COMPF"  : instruction(0x88, 3),
    "COMPR"  : instruction(0xA0, 2),
    "DIV"    : instruction(0x24, 3),
    "DIVF"   : instruction(0x64, 3),
    "DIVR"   : instruction(0x9C, 2),
    "FIX"    : instruction(0xC4, 1),
    "FLOAT"  : instruction(0xC0, 1),
    "HIO"    : instruction(0xF4, 1),
    "J"      : instruction(0x3C, 3),
    "JEQ"    : instruction(0x30, 3),
    "JGT"    : instruction(0x34, 3),
    "JLT"    : instruction(0x38, 3),
    "JSUB"   : instruction(0x48, 3),
    "LDA"    : instruction(0x00, 3),
    "LDB"    : instruction(0x68, 3),
    "LDCH"   : instruction(0x50, 3),
    "LDF"    : instruction(0x70, 3),
    "LDL"    : instruction(0x08, 3),
    "LDS"    : instruction(0x6C, 3),
    "LDT"    : instruction(0x74, 3),
    "LDX"    : instruction(0x04, 3),
    "LPS"    : instruction(0xD0, 3),
    "MUL"    : instruction(0x20, 3),
    "MULF"   : instruction(0x60, 3),
    "MULR"   : instruction(0x98, 2),
    "NORM"   : instruction(0xC8, 1),
    "OR"     : instruction(0x44, 3),
    "RD"     : instruction(0xD8, 3),
    "RMO"    : instruction(0xAC, 2),
    "RSUB"   : instruction(0x4C, 3),
    "SHIFTL" : instruction(0xA4, 2),
    "SHIFTR" : instruction(0xA8, 2),
    "SIO"    : instruction(0xF0, 1),
    "SSK"    : instruction(0xEC, 3),
    "STA"    : instruction(0x0C, 3),
    "STB"    : instruction(0x78, 3),
    "STCH"   : instruction(0x54, 3),
    "STF"    : instruction(0x80, 3),
    "STI"    : instruction(0xD4, 3),
    "STL"    : instruction(0x14, 3),
    "STS"    : instruction(0x7C, 3),
    "STSW"   : instruction(0xE8, 3),
    "STT"    : instruction(0x84, 3),
    "STX"    : instruction(0x10, 3),
    "SUB"    : instruction(0x1C, 3),
    "SUBF"   : instruction(0x5C, 3),
    "SUBR"   : instruction(0x94, 2),
    "SVC"    : instruction(0xB0, 2),
    "TD"     : instruction(0xE0, 3),
    "TIO"    : instruction(0xF8, 1),
    "TIX"    : instruction(0x2C, 3),
    "TIXR"   : instruction(0xB8, 2),
    "WD"     : instruction(0xDC, 3),
}

print(OPTAB["ADD"])