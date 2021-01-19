from src.number import Number
class LiteralTable:
    def __init__(self,main, Name, value=None,Address=None):
        self.Name, self.value, self.Address = Name, value, Address
        self.t=0
        self.ref_to=None
        if self.Name not in [i.Name for i in main.litpool]:
            self.calc_value()
            main.litpool.append(self)
      #      print(str(self))
    def calc_value(self):
        temp=self.Name
        if temp[0].upper() == 'C':
            self.t = 0
            #convert chars to hex
            self.value= Number(temp[2:-1]).chars_to_hex()
            
        elif temp[0].upper() == 'X':
            if Number(temp[2:-1]).test_hex() == False:
                raise Exception(
                    f"{temp}\t  value must to be hex")
            self.t = 1
            self.value = self.Name[2:-1]
        elif Number(temp).is_int():  # int
            self.t = 2
            self.value = temp[2:1]
        else:
            raise Exception(f" formate {type(temp[0])} is undefined")

    def __str__(self) -> str:
        return "=%-6s  |" % (self.Name)+"  %9s  |" % (self.value) + \
                "\t%-6s" % (self.Address)



    @staticmethod
    def get(main,Address):
      #  print("sssssssssssssssssssssssssssssss")
        temp = main.litpool[0]
        main.litpool = main.litpool[1:]
        temp.Address = Address
        main.litpoolTable.append(temp)
     #   print(str(temp))
        return temp


