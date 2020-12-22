from src.Files import File

f=File("Files\inSICXE.txt")
data=f.read(start_ign=['.'])
print(f.read(start_ign=['.'])[1])
new_f=File("Files\\test.txt")
new_f.write(data_str="hte\nhello")

