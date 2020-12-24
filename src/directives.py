from main import Main
from .number import Number
from .models.Lines import Line as l
class Directives:
    def __init__(self,main:Main):
        self.main=main
        self.linef=lambda c,size : Number(Number(self.main.current_loc).int()+c).hex(size=size)
    
    def handel(self,line,part):
        if(str(part).upper()) == "START":
            self.start(line)
        elif(str(part).upper()) == "END":
            self.end(line)
        elif(str(part).upper()) == "BYTE":
            self.byte(line)




    def byte(self,line):
        if "BYTE" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of LABEL can't to set as BYTE")
        elif len(line) > 3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong BYTE formate")  
        elif  line.count("BYTE") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] BYTE position")
        elif line[0].upper() in self.main.symtab:
            raise Exception(f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")
        else:
            #nshof hya c walla x
            temp=line[2]
            if temp[0].upper() == 'C':
                #convert chars to hex
                hex=Number(temp[2:-1]).chars_to_hex()
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "BYTE",
                        True
                    )
                )
                self.main.symtab[line[0].upper()]=self.main.current_loc
                self.main.current_loc = self.linef(len(temp[2:-1]),6)
            elif temp[0].upper() == 'X':
                if Number(temp[2:-1]).test_hex() == False:
                    raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
            else:
                raise Exception(f"LINE[{ self.main.lineno}]\tformate {temp[0]} is undefined")

    def end(self,line):
        if "END" != line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse END position")
        elif line[1] == "END":
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of END pointer can't to set as END")
        
        #TODO nshof el location dah sa7 bel vars aw 3ady walla la

        else:
             self.main.Lines.append(
                l(
                    line,
                    self.main.lineno,
                    self.main.current_loc,
                    "END",
                    True
                )
            )

    def start(self,line):
        print(line)
        if "START" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of prog can't to set as START")
        elif "START" == line[2].upper():
            raise Exception(f"LINE[{self.main.lineno}]\tFalse START position")
        elif len(line[0]) > 6:
            raise Exception(f"LINE[{self.main.lineno}]\tname is more than 6 chars")
        elif Number(line[2]).test_hex() == False:
            raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
        else:
                self.main.start_addr=Number(line[2]).hex_size(size=6)
                self.main.current_loc=self.main.start_addr
                self.main.name=line[0]
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "START",
                        True
                    )
                )
                self.main.current_loc = self.linef(4,6)
                print( self.main.current_loc)

