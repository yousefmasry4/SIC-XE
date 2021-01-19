from src.number import Number
from src.Files import File
import string
from .Instruction import instruction as inst


class Line:
    def __init__(self, instruction, noL, location, instr=None, asm=False, label=None, ref=None, object_code=None,
                 inst_object=None, formate=None, have_x=False, pre=None, stm_type="R"):

        self.instruction_list = instruction
        self.instruction = instr
        self.asm=asm
        self.label = label
        self.ref = ref
        self.object_code = object_code
        self.inst_object = inst_object
        self.formate = formate
        self.have_x = have_x
        self.noL = noL  # line number
        self.location = location
        self.pre = pre


        self.n=0
        self.i=0
        self.x=0
        self.b=0
        self.p=0
        self.e=0


        if not asm:
            temp = inst(self.instruction_list)
            self.formate = temp.formate
            self.inst_object = temp.opcode
            self.instruction = temp.instruct
            self.have_x=temp.have_x
            self.label = temp.label
            if (temp.ref != None):
                self.pre, self.ref = self.operand_pre(temp.ref)


        else:
            # TODO pass2 zbt el opcode w el 7gat dy
            if self.instruction.upper() != "EQU" and self.instruction[0] != "=":
                self.pre, self.ref = self.operand_pre(self.ref)

    def operand_pre(self, op):
        #  print(op)
        if (op == None):
            return None, None
        if not (op[0].upper().isalpha() or Number(op[0]).is_int()):
            #      print("wwwwwwwwwww")
            if op[0] == "@" or op[0] == "#" or op[0] == "=":
                #             print("ss")
                return op[0], op[1:]
            else:
                raise Exception(f" {op[0]}\tis not defined")

        else:
            return None, op

    def __str__(self):
        return " ".join("%-2s\t" % self.noL
                        + "%-9s\t" % (self.location[2:].upper() if self.location != None else "")
                        + "%-9s\t" % (self.label if self.label != None else "")
                        + "%-9s\t" % (self.instruction if self.instruction != None else "")
                        + "%+1s" % (self.pre if self.pre != None else "")
                        + "%-9s\t" % (self.ref if self.ref != None else "")
                        + "%s" % (self.object_code if self.object_code is not None  else "----------")
                        )
