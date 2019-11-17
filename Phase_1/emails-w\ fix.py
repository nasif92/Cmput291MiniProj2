f = open("1k.xml","r")
init_data = []
from_seg = []
to_seg = []
rows = []
chad = []
A_list = []
CC_list = []
BCC_list = []

for line in f:
    init_data.append(line)
    #print(init_data)

del init_data[0], init_data[0], init_data[-1]

for test in init_data:
    y = test.index("<mail>")
    er = test.index("</mail>")
    A_list.append(test[y:er])
    
#print(A_list)
for testy in A_list:
    m = testy.index("<from>")
    n = testy.index("</from>")
    o = testy.index("<to>")
    p = testy.index("</to>")
    c = testy.index("<row>")
    u = testy.index("</row>")
    from_seg.append(testy[m+6:n])
    to_seg.append(testy[o+4:p])
    rows.append(testy[c+5:u])   
    if "<cc>" in  testy:
        #print(testy)
        #print()
        cc = testy.index("<cc>")
        cca = testy.index("</cc>")
        string = testy[cc+4:cca]
        #print(testy[cc+4:cca])
        #if "," in string:
            #string = string.replace(',','\n')
            #print(string)CC_list[b] 


        #testy[cc+4:cca]
        CC_list.append(string)
    if "<bcc>" in testy:
        bcc = testy.index("<bcc>")
        bcca = testy.index("</bcc>")
        BCC_list.append(testy[bcc+5:bcca])
    

    
    
#print("FROM", from_seg)
#print("TO", to_seg)
#print("ROWS", rows)
#print("CC", CC_list)
#print("BCC", BCC_list)


for b in range(0,len(to_seg)):
    fro = "from-"
    to = "to-"  
    cc_string = "cc-"
    bcc_string = "bcc-"
    fro = fro + from_seg[b] + ":" + rows[b]
    to = to + to_seg[b] + ":" + rows[b]
    fro = fro + "\n" + to
    
    #craig.brown@enron.com\n;row
    #colleen.koenig@enron.com\njennifer.medcalf@enron.com\nsarah-joy.hunter@enron.com
    if CC_list[b] != "":
        #if "\n" in CC_list[b]:
            #CC_list[b].replace("\n",":" + rows[b]+"\n"+cc_string)
            #print(CC_list[b])
        cc_string = cc_string + CC_list[b] + ":" + rows[b]
        fro= fro+ "\n" + cc_string
    if BCC_list[b] != "":
        bcc_string = bcc_string + BCC_list[b] + ":" + rows[b]
        fro = fro +"\n"+bcc_string
    chad.append(fro)
            
#print(chad)



g = open("email1k.txt","w+")

for i in range(0,len(chad)):
    g.write(chad[i]+ "\n")

    
g.close()
    




#print(init_data)


