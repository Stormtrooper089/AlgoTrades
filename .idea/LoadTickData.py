def loadTickData(path):
    file=open(path,'r')
    list=[]
    for line in file:
        entry = []
        a=line.split(",")
        for key in a:
            entry.append(key.strip("\n"))
        list.append(entry)
    return list