import subprocess
import os

f=open('lswifi1.log','w')
subprocess.run(["C:\\Python39\\Scripts\\lswifi"], stdout=f)
f.close()

f=open('lswifi1.log','r')
lines=f.readlines()
i=0
for line in lines:
    if(line[0]=='-'):
        ind=i
    i=i+1

for i in range(ind+1):
    lines.pop(0)

info=[]
for line in lines:
    tmp=line.split()
    for word in tmp :
        if (tmp[1].find(":")==-1):
            tmp.pop(1)
            print(tmp)
            
    info.append(tmp[0:3]+[tmp[5]])
