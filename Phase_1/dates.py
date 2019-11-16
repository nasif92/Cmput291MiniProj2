f = open("1k.xml","r")
init_data = []
date = []
rows = []
final = []


for line in f:
    init_data.append(line)
    #print(init_data)

del init_data[0], init_data[0], init_data[-1]

for line in init_data:
    #print(line)
    m = line.index("<date>")
    n = line.index("</date>")
    c = line.index("<row>")
    u = line.index("</row>")
    
    date.append(line[m+6:n])
    rows.append(line[c+5:u])
    
#print(date)


for i in range(0,len(date)):
    v = ""
    v = v + date[i] + ":" + rows[i]
    final.append(v)
    
print(final)

g = open("dates10.txt","w+")

for i in range(0,len(final)):
    g.write(final[i]+ "\n")

    
g.close()
    

