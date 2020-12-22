from src.Files import File
from Instruction import instruction as inst
class Line:
    def __init__(self, instruction,noL):
        self.instruction_list=File.split_line(instruction)
        self.instruction=inst(self.instruction_list)
        self.noL = noL # line number
        self.location=None

    def __str__(self):
        return " ".join(self.instruction_list)
