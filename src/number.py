class Number:
    def __init__(self,operand):
        self.operand=operand
    
    def hex(self):#int to hex
        return hex(self.operand)
    
    def int(self):#int to hex
        if self.operand[1] == "x" and self.operand[0] == "0":
            return int(self.operand, 0)
        else:
            return int(self.operand, 16)
    
    def bin(self):#hex to bin
        return bin(int(self.operand, 16)).zfill(8) 

    def test_hex(self):
        try:
            _ = int(self.operand, 16)
            return True
        except :
            return False

    def hex_size(self,size=5):
        if self.operand[1] == "x" and self.operand[0] == "0":
            self.operand=self.operand[2:]
            return "0x"+"0"*(0 if size - len(self.operand) <= 0 else size - len(self.operand))+self.operand
        else:
            return "0"*(0 if size - len(self.operand) <= 0 else size - len(self.operand))+self.operand