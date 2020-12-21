a=int(time.time())
periode=15
data = {'aaaaa':15,'bbbb':30,'ccccc':30,'ddddd':60}
lastsenttime = {}
tunggu=False
lastsend=0
while True:
     skrg = int(time.time())
     for i in data:
        try:
            ck = lastsenttime[i]
        except:
            lastsenttime[i]=0
        if ((skrg-a)%data[i]==0) and ( lastsenttime[i]!=skrg ):
           lastsenttime[i] = skrg
           print(i+' '+str(skrg))
