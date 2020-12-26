from src.number import Number
class LiteralTable:
    def __init__(self,main, Name, value=None,Address=None):
        self.Name, self.value, self.Address = Name, value, Address
        self.t=0
        if self.Name not in main.litpool:
            main.litpool.append(self)
            self.calc_value()
    
    def calc_value(self):
        temp=self.Name[1:]
        if temp[0].upper() == 'C':
            self.t = 0
            #convert chars to hex
            self.value= Number(temp[2:-1]).chars_to_hex()
            
        elif temp[0].upper() == 'X':
            if Number(temp[2:-1]).test_hex() == False:
                raise Exception(
                    f"{temp}\t  value must to be hex")
            else:
                self.t = 1
                self.value = temp[2:1]
        elif Number(temp).is_int():  # int
            self.t = 2
            self.value = temp[2:1]
        else:
            raise Exception(f" formate {type(temp[0])} is undefined")

    @staticmethod
    def get(main,Address):
        temp = main.litpool[0]
        main.litpool = main.litpool[1:]
        temp.Address = Address
        main.litpoolTable.append(temp)
        return temp
