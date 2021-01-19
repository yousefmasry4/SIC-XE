from .models.Lines import Line as l
from .number import Number


class Pass2:

    def __init__(self, arr, i, labels, base):
        self.PRELOAD_SYMTAB = {
            "A": 0,
            "X": 1,
            "B": 3,
            "S": 4,
            "T": 5,
            "F": 6,
        }
        self.line = arr[i]
        self.labels = labels
        self.base = base
        self.be = None

        for lll in arr[i + 1:]:
            #   print(">>>",lll.location)
            if lll.location is None:
                continue
            else:
                self.be = lll.location
                break
        print("qqqqqqqqqqqqqqqqqqqqqqqqq", self.line.ref, "j")
        self.detected_lit = None
        self.dis = None

        self.detect_lit()

        self.go_lit() if self.detected_lit else self.normal()

        self.line.x = 1 if self.line.have_x else 0
        if self.line.formate == 3 or self.line.formate == 4:
            if self.line.pre == "#":
                self.line.i = 1
            elif self.line.pre == "@":
                self.line.n = 1
            else:
                self.line.i = 1
                self.line.n = 1
        elif self.line.formate == 2:
            data = self.line.ref.split(",")
            a = self.PRELOAD_SYMTAB[data[0]]
            b = 0
            if len(data) != 1:
                b = self.PRELOAD_SYMTAB[data[1]]
            print(self.line.inst_object)
            self.line.object_code = "{0}{1}{2}".format(
                Number(self.line.inst_object).hex()[-2:],
                str(a),
                str(b)
            ).upper()

        if self.line.formate == 4:
            self.line.e = 1
            self.line.p = 0
            self.line.b = 0
            print(self.line.inst_object)
            suyo = self.line.ref
            print("43********************", suyo)
            if "#" != self.line.pre:
                self.line.object_code = self.labels[suyo]
                self.line.object_code = "%6s" % ("%s" % (Number(int("{0}{1}{2}{3}{4}{5}{6}".format(
                    ("%7s" % bin(self.line.inst_object)[2:-2]), str(self.line.n),
                    str(self.line.i),
                    str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)),
                    2)).hex() +
                                                         self.line.object_code[-5:]
                                                         ).upper()).replace(" ", "0")[2:]
            else:
                sy = Number(int(suyo)).hex(size=5)[2:]

                self.line.object_code = "%6s" % ("%s" % (Number(int("{0}{1}{2}{3}{4}{5}{6}".format(
                    ("%7s" % bin(self.line.inst_object)[2:-2]), str(self.line.n),
                    str(self.line.i),
                    str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)),
                    2)).hex() +
                                                         sy
                                                         ).upper()).replace(" ", "0")[2:]

        elif self.line.formate == 3:
            if self.line.pre == "#" and Number(self.line.ref).is_int():
                self.line.object_code = "%6s" % ("%6s" % (Number(int("{0}{1}{2}{3}{4}{5}{6}".format(
                    ("%6s" % bin(self.line.inst_object)[2:-2]).replace(" ", "0"), str(self.line.n),
                    str(self.line.i),
                    str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)),
                    2)).hex() + Number(int(self.line.ref if self.line.have_x == False else self.line.ref[:-2])).hex(
                    size=3)[-3:]).upper()).replace(" ", "0")[2:]
                self.line.object_code = self.line.object_code.replace(" ", "0")

            elif "RSUB" == self.line.instruction_list[0]:
                self.line.object_code = "4F0000"
            else:
                self.calc_dis()
                print(")-", self.dis)
                self.line.object_code = ("%6s" % (Number(int("{0}{1}{2}{3}{4}{5}{6}".format(
                    ("%6s" % bin(self.line.inst_object)[2:-2]).replace(" ", "0"), str(self.line.n), str(self.line.i),
                    str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)), 2)).hex() + (
                                                      self.dis[-3:]))[
                                                 2:].upper()).replace(" ", "0")
            print(self.line.instruction_list, ("%s" % ("{0}{1}{2}{3}{4}{5}{6}".format(
                ("%6s" % bin(self.line.inst_object)[2:-2]).replace(" ", "0"), str(self.line.n), str(self.line.i),
                str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)))
            [:].upper())
                  )
        elif self.line.formate == 5:
            if "@" in self.line.ref or "#" in self.line.ref:
                raise Exception(f"LINE[{self.line.noL}]\tThis format neither supports immediate nor indirect "
                                f"addressing modes. {self.line.instruction_list}")
            self.calc_dis()
            dis = ("%12s" % self.dis[-3:]).replace(" ", "0")
            f1, f2 = "1" if Number(dis).int() % 2 == 0 else "0", "1" if Number(dis).int() > 0 else "0"
            self.line.object_code = (Number(int("{0}{1}{2}{3}{4}{5}{6}".format(
                ("%6s" % bin(self.line.inst_object)[2:-2]).replace(" ", "0"), f1, f2,
                str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)), 2)).hex() + dis[-3:]).upper()[2:]

            print("Saddddddddd",dis)
            print("{0}/{1}{2}{3}{4}{5}{6}".format(
                ("%6s" % bin(self.line.inst_object)[2:-2]).replace(" ", "0"), f1, f2,
                str(self.line.x), str(self.line.b), str(self.line.p), str(self.line.e)))

    #    print("~~", self.line.location) ) and size != 3

    def detect_lit(self):
        self.detected_lit = self.line.pre == '='

    def go_lit(self):
        pass

    def normal(self):
        pass

    def calc_dis(self):

        print(self.line.ref)
        print(self.line.ref if self.line.have_x == False else self.line.ref[:-2])
#        print("81/////", self.labels[self.line.ref if self.line.have_x == False else self.line.ref[:-2]])
        self.dis = Number(self.labels[self.line.ref if self.line.have_x == False else self.line.ref[:-2]]).int()
        self.dis -= Number(self.be).int()
        print(Number(self.labels[self.line.ref if self.line.have_x == False else self.line.ref[:-2]]).int(), "-",
              Number(self.be).int(), " = ", self.dis)
        if 2048 >= self.dis >= -2048:
            self.line.p = 1
            if self.dis < 0:
                self.dis = hex(self.dis & (2 ** 32 - 1))[-3:]
            else:
                self.dis = Number(self.dis).hex(size=6)
            print("****>>", self.dis)
        else:
            print("type 222222222222222222222",self.labels[self.line.ref if self.line.have_x == False else self.line.ref[:-2]],Number(
                    self.base).int())
            self.line.b = 1
            self.dis = Number(
                Number(self.labels[self.line.ref if self.line.have_x == False else self.line.ref[:-2]]).int() - Number(
                    self.base).int()).hex(size=6)
