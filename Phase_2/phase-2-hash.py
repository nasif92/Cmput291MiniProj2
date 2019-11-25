#Meant to create the 4 needed txt files for db_load in one program
#SORT COMMANDS:
# DATES: sort -u dates.txt -o sorteddates.txt
# EMAILS: sort -u emails.txt -o sortedemails.txt
# RECS: sort -nu recs10.txt -o sortedrecs.txt
# TERMS: sort -u terms.txt -o sortedterms.txt


# To use db_load properly, assuming you installed everything needed:
# RECS: db_load -T -c duplicates=1 -f recsfinal.txt -t hash re.idx
# EMAILS: db_load -T -c duplicates=1 -f emailsfinal.txt -t btree em.idx
# DATES: db_load -T -c duplicates=1 -f datesfinal.txt -t btree da.idx
# TERMS: db_load -T -c duplicates=1 -f termsfinal.txt -t btree da.idx

#RECS
f = open("sortedrecs.txt","r")
init_data = []



for line in f:
    line = line.replace("\\", "")

    line = line.replace(":", "\n",1)
    init_data.append(line)


    

g = open("recsfinal.txt","w+")
                
for i in range(0,len(init_data)):
    g.write(init_data[i]+ "")
                
                    
g.close()


#DATES
f = open("sorteddates.txt","r")
init_data = []

for line in f:
    line = line.replace("\\", "")

    line = line.replace(":", "\n",1)
    init_data.append(line)


    

g = open("datesfinal.txt","w+")
                
for i in range(0,len(init_data)):
    g.write(init_data[i]+ "")
                
                    
g.close()

#EMAILS

f = open("sortedemails.txt","r")
init_data = []

for line in f:
    line = line.replace("\\", "")

    line = line.replace(":", "\n",1)
    init_data.append(line)


    

g = open("emailsfinal.txt","w+")
                
for i in range(0,len(init_data)):
    g.write(init_data[i]+ "")
                
                    
g.close()


# TERMS

f = open("sortedterms.txt","r")
init_data = []

for line in f:
    line = line.replace("\\", "")

    line = line.replace(":", "\n",1)
    init_data.append(line)


    

g = open("termsfinal.txt","w+")
                
for i in range(0,len(init_data)):
    g.write(init_data[i]+ "")
                
                    
g.close()

print("Finished")


