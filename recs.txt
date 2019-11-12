f = open("10.xml","r")
init_data = []
date = []
rows = []
chad = []

for line in f:
    init_data.append(line)
    #print(init_data)

del init_data[0], init_data[0], init_data[-1]

for line in init_data:
    
    m = line.index("<mail>")
    n = line.index("</mail>")
    c = line.index("<row>")
    u = line.index("</row>")  
    
    date.append(line[m:n+7])
    rows.append(line[c+5:u])    
    
print(date)
print(rows)

for i in range(0,len(date)):
    v = ""
    v = v + rows[i] + ":" + date[i]  
    chad.append(v)
    
print(chad)

g = open("recs10.txt","w+")

for i in range(0,len(chad)):
    g.write(chad[i]+ "\n")

    
g.close()