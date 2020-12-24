from src.Files import File
from .Instruction import instruction as inst
class Line:
    def __init__(self,instruction,noL,location,instr=None,asm=False):
        self.instruction_list=instruction
        self.instruction=instr
        if not asm:
            self.instruction=inst(self.instruction_list)
        else:
            #TODO pass2 zbt el opcode w el 7gat dy
            pass
        self.noL = noL # line number
        self.location=location

    def __str__(self):
        return " ".join(self.instruction_list)
