f = open("10.xml","r")
init_data = []
body = []
rows = []
subj = []
chad = []
A_list = []
xa = []
for line in f:
    init_data.append(line)
#print(init_data)
#print('\n')
#print('\n')

del init_data[0], init_data[0], init_data[-1]

for test in init_data:
    y = test.index("<mail>")
    er = test.index("</mail>")
    xa = test[y:er].replace("&lt;", "<")
    xa = test[y:er].replace("&gt;", ">")
    xa = test[y:er].replace("&amp;", "&")
    xa = test[y:er].replace("&apos;", "'")
    xa = test[y:er].replace("&quot;", '"')
    
    
    A_list.append(xa)
#print(A_list[1]+'\n')
for line in A_list:
    o = line.index("<subj>")
    p = line.index("</subj>")
    m = line.index("<body>")
    n = line.index("</body>")
    c = line.index("<row>")
    u = line.index("</row>") 
    
    emp = line[o+6:p].lower()
    emp = emp.replace("&#10;"," ")
    emp = emp.replace(",", " ")
    emp = emp.replace(":", " ")
    emp = emp.replace(".", " ")
    emp = emp.replace("/"," ")
    emp = emp.replace("&"," ")
    emp = emp.replace("'"," ")
    emp = emp.replace('"'," ")
    emp = emp.split() 

    #print(emp) 
    for v in emp:
        if v[0] != "&" and x != "" and len(v) > 2:
            body.append("s-" + v + ":" + line[c+5:u])
            
    emp = line[m+6:n].lower()
    emp = emp.replace("&apos;"," ")
    emp = emp.replace("&amp;"," ")
    emp = emp.replace("&#10;"," ")
    emp = emp.replace("?"," ")
    emp = emp.replace(",", " ")
    emp = emp.replace(":", " ")
    emp = emp.replace(".", " ")
    emp = emp.replace("/"," ")
    emp = emp.replace("&"," ")
    emp = emp.replace("'"," ")
    emp = emp.replace('"'," ")    
    emp = emp.split()
    for x in emp:
        if x[0] != "&" and x != "" and len(x) > 2:
            body.append("b-" + x  + ":" + line[c+5:u])

print(body)
            



g = open("terms10.txt","w+")
            
for i in range(0,len(body)):
    g.write(body[i]+ "\n")
            
                
g.close()