from .number import Number
from .models.Lines import Line as l
from math import ceil
from src.models.literalTable import LiteralTable
import string
class Directives:
    def __init__(self,main):
        self.main=main
        self.linef=lambda c,size : Number(Number(self.main.current_loc).int()+c).hex(size=size)
    


    def handel(self,line,part):
        if(str(part).upper()) == "START":
            self.start(line)
        elif(str(part).upper()) == "END":
            self.end(line)
        elif(str(part).upper()) == "BYTE":
            self.byte(line)
        elif(str(part).upper()) == "WORD":
            self.word(line)
        elif(str(part).upper()) == "RESW":
            self.RESW(line)
        elif(str(part).upper()) == "BASE":
            self.BASE(line)
        elif(str(part).upper()) == "RESB":
            self.RESB(line)
        elif(str(part).upper()) == "EQU":
            self.EQU(line)
        elif(str(part).upper()) == "LTORG":
            self.LTORG(line)

    def LTORG(self, line):
        if len(line) >1:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong LTORG formate")
        else:
            self.main.Lines.append(
                l(
                    line,
                    self.main.lineno,
                    self.main.current_loc,
                    "LTORG",
                    True,
                    ref=None,
                    label=None
                )
            )
            self.GOoRG()

    def GOoRG(self):
        while(len(self.main.littab) != 0):
            self.main.lineno += 1
            t=LiteralTable.get(self.main, self.main.current_loc)
            self.main.Lines.append(
                l(
                    ["*",t.Name],
                    self.main.lineno,
                    self.main.current_loc,
                    t.Name,
                    True,
                    ref="*",
                    label=None
                )
            )
            self.main.current_loc = self.linef(ceil(len(t.value)/2), 6)

    def EQU(self, line):
        if "EQU" != line[1].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\twrong EQU location")
        elif len(line) !=3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong EQU formate")
        elif [i.upper() for i in line].count("EQU") > 1:
            raise Exception(
                f"LINE[{ self.main.lineno}]\tFalse [Multiple] EQU position")
        elif line[0].upper() in self.main.symtab and self.main.symtab[line[0].upper()] != None:
            raise Exception(
                f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")
        else:
            if line[2] == "*":
                self.main.symtab[line[0]] = self.main.current_loc
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        None,
                        "EQU",
                        True,
                        ref=line[2],
                        label=line[0]
                    )
                )
            else:#equation
                eq=line[2]
                list_eq=eq.replace("-","+").split("+")
                try:
                    a, b = self.main.symtab[list_eq[0]
                                            ], self.main.symtab[list_eq[1]]
                    ans = Number(Number(a).int() + (Number(b).int()
                                                    if "+" in eq else Number(b).int()*-1)).hex(size=6)

                    self.main.symtab[line[0]] = ans
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            None,
                            "EQU",
                            True,
                            ref=line[2],
                            stm_type="A",
                            label=line[0]
                        )
                    )
                    self.main.sTypeA.append(line[0])
                        
                except:
                    raise Exception(
                        f"LINE[{ self.main.lineno}]\t bad vars {eq}")                   

    def BASE(self,line):
        if "BASE" != line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\twrong BASE location")
        elif len(line) > 2:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong BASE formate")  
        elif  [i.upper() for i in line].count("BASE") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] BASE position")
        else:
            if line[1].upper() not in self.main.symtab:
                self.main.symtab[line[1].upper()]=None
           # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            self.main.base= self.main.symtab[line[1].upper()]
            self.main.Lines.append(
                l(
                    line,
                    self.main.lineno,
                    None,
                    "BASE",
                    True,
                    ref=line[1]
                )
            )


    def RESW(self,line):
        if "RESW" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of LABEL can't to set as RESW")
        elif len(line) > 3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong RESW formate")  
        elif  [i.upper() for i in line].count("RESW") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] RESW position")
        elif line[0].upper() in self.main.symtab and self.main.symtab[line[0].upper()] != None:
            raise Exception(f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")      
        else:
            #nshof hya c walla x
            temp=line[2]
            self.main.symtab[line[0].upper()]=self.main.current_loc
         #   print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
         #   print(self.main.symtab[line[0].upper()])
            if temp[0].upper() == 'C':
                #convert chars to hex
                hex=Number(temp[2:-1]).chars_to_hex()
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "RESW",
                        True,
                        ref=temp,
                        label=line[0]

                    )
                )
                self.main.current_loc = self.linef(Number(hex).int()*3,6)
            elif temp[0].upper() == 'X':
                if Number(temp[2:-1]).test_hex() == False:
                    raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
                else:
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "RESW",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(Number(temp[2:-1]).int()*3,6)
            elif Number(temp).is_int():#int
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "RESW",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(int(temp)*3,6)               
            else:
      #          print(Number(temp).test_hex())
                raise Exception(f"LINE[{ self.main.lineno}]\tformate {type(temp[0])} is undefined")    


    def RESB(self,line):
   #     print(
    #        "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        if "RESB" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of LABEL can't to set as RESB")
        elif len(line) > 3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong RESB formate")  
        elif  [i.upper() for i in line].count("RESB") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] RESB position")
        elif line[0].upper() in self.main.symtab and (self.main.symtab[line[0].upper()]!=None):
            raise Exception(f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")      
        else:
  #          print(
 #               "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    #        print(line)
            #nshof hya c walla x
            temp=line[2]
            self.main.symtab[line[0].upper()]=self.main.current_loc
            if temp[0].upper() == 'C':
                #convert chars to hex
                hex=Number(temp[2:-1]).chars_to_hex()
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "RESB",
                        True,
                        ref=temp,
                        label=line[0]
                    )
                )
                self.main.current_loc = self.linef(Number(hex).int(),6)
            elif temp[0].upper() == 'X':
                if Number(temp[2:-1]).test_hex() == False:
                    raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
                else:
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "RESB",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(Number(temp[2:-1]).int(),6)
            elif Number(temp).is_int():#int

                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "RESB",
                        True,
                        ref=temp,
                        label=line[0]
                    )
                )
                
                self.main.current_loc = self.linef(int(temp),6)               
            else:
                raise Exception(f"LINE[{ self.main.lineno}]\tformate {temp[0]} is undefined")    



    def word(self,line):
        if "WORD" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of LABEL can't to set as WORD")
        elif len(line) > 3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong WORD formate")  
        elif  [i.upper() for i in line].count("WORD") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] WORD position")
        elif line[0].upper() in self.main.symtab and (self.main.symtab[line[0].upper()]!=None):
            raise Exception(f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")      
        else:
            #nshof hya c walla x
            temp=line[2]
            self.main.symtab[line[0].upper()]=self.main.current_loc
            if temp[0].upper() == 'C':
                #convert chars to hex
                hex=Number(temp[2:-1]).chars_to_hex()
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "WORD",
                        True,
                        ref=temp,
                        label=line[0]
                    )
                )
                self.main.current_loc = self.linef(3,6)
            elif temp[0].upper() == 'X':
                if Number(temp[2:-1]).test_hex() == False:
                    raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
                else:
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "WORD",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(3,6)
            elif Number(temp).is_int():#int
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "WORD",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(3,6)               
            else:
                raise Exception(f"LINE[{ self.main.lineno}]\tformate {temp[0]} is undefined")             

    def byte(self,line):
        if "BYTE" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of LABEL can't to set as BYTE")
        elif len(line) > 3:
            raise Exception(f"LINE[{ self.main.lineno}]\tWrong BYTE formate")  
        elif  [i.upper() for i in line].count("BYTE") > 1:
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse [Multiple] BYTE position")
        elif line[0].upper() in self.main.symtab and (self.main.symtab[line[0].upper()]!=None):
    #            print(line[0].upper(),self.main.symtab[line[0].upper()])
                raise Exception(f"LINE[{ self.main.lineno}]\tMULTI useing of label {line[0]}")
        else:
            #nshof hya c walla x
            temp=line[2]
            self.main.symtab[line[0].upper()]=self.main.current_loc
            if temp[0].upper() == 'C':
                #convert chars to hex
                hex=Number(temp[2:-1]).chars_to_hex()
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        self.main.current_loc,
                        "BYTE",
                        True,
                        ref=temp,
                        label=line[0]
                    )
                )
                self.main.current_loc = self.linef(len(temp[2:-1]),6)
            elif temp[0].upper() == 'X':
                if Number(temp[2:-1]).test_hex() == False:
                    raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
                else:
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "BYTE",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(ceil(len(temp[2:-1])/2),6)
            elif Number(temp).is_int():#int
                    self.main.Lines.append(
                        l(
                            line,
                            self.main.lineno,
                            self.main.current_loc,
                            "BYTE",
                            True,
                            ref=temp,
                            label=line[0]
                        )
                    )
                    self.main.current_loc = self.linef(ceil(len(Number(temp).hex())/2),6)               
            else:
                raise Exception(f"LINE[{ self.main.lineno}]\tformate {temp[0]} is undefined")

    def end(self,line):
        if "END" != line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tFalse END position")
        elif line[1] == "END":
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of END pointer can't to set as END")
        elif (self.main.symtab[line[1].upper()]!= self.main.start_addr ):
     #       print(self.main.symtab[line[1].upper()])
            raise Exception(f"LINE[{ self.main.lineno}]\t wrong value")     
        else:
            self.main.Lines.append(
                l(
                    line,
                    self.main.lineno,
                    None,
                    "END",
                    True,
                    ref=line[1]
                )
            )
            self.GOoRG()



    def start(self,line):
    #    print(line)
        if "START" == line[0].upper():
            raise Exception(f"LINE[{ self.main.lineno}]\tthe name of prog can't to set as START")
        elif "START" == line[2].upper():
            raise Exception(f"LINE[{self.main.lineno}]\tFalse START position")
        elif len(line[0]) > 6:
            raise Exception(f"LINE[{self.main.lineno}]\tname is more than 6 chars")
        elif Number(line[2]).test_hex() == False:
            raise Exception(f"LINE[{self.main.lineno}]\t starting address must to be hex")
        else:
                self.main.start_addr=Number("0x"+line[2]).hex_size(size=6)
                self.main.current_loc=self.main.start_addr
                self.main.name=line[0]
              #  self.main.symtab[self.main.name.upper()] = self.main.current_loc
              #  print("start ", line)
                self.main.Lines.append(
                    l(
                        line,
                        self.main.lineno,
                        None,
                        "START",
                        asm=True,
                        formate=3,
                        ref=line[2],
                        label=line[0]
                    )
                )
                self.main.current_loc = self.linef(0,6)

