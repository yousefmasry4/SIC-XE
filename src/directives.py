from number import Number
from models.Lines import Line as l
class Directives:
    def __init__(self):
        pass
    def handel(self,main,line,part):
        if(str(part).upper) == "START":
            self.start(main,line)


    def start(self,main,line):
        
        if "START" == line[0].upper():
            raise Exception(f"LINE[{main.lineno}]\tthe name of prog can't to set as START")
        elif "START" == line[2].upper():
            raise Exception(f"LINE[{main.lineno}]\tFalse START position")
        elif len(line[0]) > 6:
            raise Exception(f"LINE[{main.lineno}]\tname is more than 6 chars")
        elif Number(line[2]).test_hex == False:
            raise Exception(f"LINE[{main.lineno}]\t starting address must to be hex")
        else:
                main.start_addr=Number(line[2]).hex_size(size=6)
                main.current_loc=main.start_addr
                main.name=line[0]
                main.Lines.append(
                    l(
                        "START",
                        main.lineno,
                        main.current_loc,
                        True
                    )
                )
                main.current_loc = Number(Number(main.current_loc).int()+4).hex()

