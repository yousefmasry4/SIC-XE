import re
class File:
    def __init__(self,path):
        super().__init__()
        self.path=path
    def read(self , ign=[],start_ign=[]):
        return list(re.sub(' +', ' ',str(line).replace("\t",' ').replace("  "," ").strip('\n')) for line in open(self.path, "r").readlines() if line.strip('\n') not in ign and line[0] not in start_ign)
    def write(self,data_list=[],data_str=None):
        f = open(self.path, "w")
        f.write("\n".join(data_list) if data_str == None else data_str)
        f.close()
