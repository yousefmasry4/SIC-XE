class Number:
    def __init__(self,operand):
        self.operand=operand
    
    def hex(self,size=0):#int to hex
        self.operand=hex(self.operand)
        return self.operand if size == 0 else self.hex_size(size=size)
    
    def int(self):#int to hex
        if  "x" in self.operand:
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
        if  "x" in self.operand:
            self.operand=self.operand[2:]
            return "0x"+"0"*(0 if size - len(self.operand) <= 0 else size - len(self.operand))+self.operand
        else:
            return "0"*(0 if size - len(self.operand) <= 0 else size - len(self.operand))+self.operand