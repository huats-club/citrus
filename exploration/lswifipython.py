import subprocess

f = open('lswifi1.log', 'w')
subprocess.run(["C:\\Users\\65844\miniconda3\\Scripts\\lswifi"], stdout=f)
f.close()

f = open('lswifi1.log', 'r')
lines = f.readlines()

i = 0
for line in lines:
    if(line[0] == '-'):
        ind = i
    i = i+1

for i in range(ind+1):
    lines.pop(0)

# info = []
# for line in lines:
#     tmp = line.split()
#     for word in tmp:
#         if (tmp[1].find(":") == -1):
#             tmp.pop(1)
#             print(tmp)

#  info.append(tmp[0:3]+[tmp[5]])

final = []
for line in lines:
    tmp = line.split()
    print(tmp)
    for word in tmp:
        if(word.find(':') != -1 and len(word) > 15):
            print(word)
            ind = (tmp.index(word))
    if(ind == 0):
        tmp.insert(0, 'FUB')
        print(tmp)
    else:
        tmp.insert(0, " ".join(tmp[0:ind]))
        del tmp[1:ind+1]
        print(tmp)
    final.append(tmp)

    print(final)
