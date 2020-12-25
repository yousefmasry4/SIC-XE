from src.number import Number
from src.Files import File
from .Instruction import instruction as inst
class Line:
    def __init__(self,instruction,noL,location,instr=None,asm=False,label=None,ref=None,object_code=None,inst_object=None,formate=None,have_x=False):
        
        
        self.instruction_list=instruction
        self.instruction=instr
        
        self.label=label
        self.ref=ref
        self.object_code=object_code
        self.inst_object=inst_object
        self.formate=formate
        self.have_x=have_x
        self.noL = noL # line number
        self.location=location
        if not asm:
            temp=inst(self.instruction_list)
            self.formate=temp.formate
            self.inst_object=temp.opcode
            self.instruction=temp.instruct
            self.label=temp.label
            self.ref=temp.ref
            
        else:
            #TODO pass2 zbt el opcode w el 7gat dy
            pass

    def __str__(self):
        return " ".join(f"{self.noL}\t"
                        +"%9s\t"%self.location
                        +"%9s\t"%self.label
                        +"%9s\t"%self.instruction
                        +"%9s\t"%Number(self.ref).hex_size(6)
                        +"%9s\t"%self.object_code
                        )
