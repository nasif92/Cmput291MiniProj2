def main():
	f = open("1k.xml","r")

	init_data = []
		
	for line in f:
		init_data.append(line)

	# each function is passed in the init data from the file
	create_emails(init_data)
	create_terms(init_data)
	create_records(init_data)
	create_dates(init_data)
	f.close()

def create_emails(init_data):
	# work for emails.txt
	
	email_list = []
	from_seg = []
	to_seg = []
	CC_list = []
	BCC_list = []
	rows = []
	chad = []


	del init_data[0], init_data[0], init_data[-1]

	for test in init_data:
		y = test.index("<mail>")
		er = test.index("</mail>")
		email_list.append(test[y:er])

	for testy in email_list:
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
			cc = testy.index("<cc>")
			cca = testy.index("</cc>")
			CC_list.append(testy[cc+4:cca])
		if "<bcc>" in testy:
			bcc = testy.index("<bcc>")
			bcca = testy.index("</bcc>")
			BCC_list.append(testy[bcc+5:bcca])
		
	# print("FROM", from_seg)
	# print("TO", to_seg)
	# print("ROWS", rows)
	# print("CC", CC_list)
	# print("BCC", BCC_list)


	for b in range(0,len(to_seg)):
		fro = "from-"
		to = "to-"  
		cc_string = "cc-"
		bcc_string = "bcc-"
		fro = fro + from_seg[b] + ":" + rows[b]
		to = to + to_seg[b] + ":" + rows[b]
		fro = fro + "\n" + to
		
		if CC_list[b] != "":
			cc_string = cc_string + CC_list[b] + ":" + rows[b]
			fro= fro+ "\n" + cc_string
		if BCC_list[b] != "":
			bcc_string = bcc_string + BCC_list[b] + ":" + rows[b]
			fro = fro +"\n"+bcc_string
		chad.append(fro)


	g = open("email10.txt","w+")

	for i in range(0,len(chad)):
		g.write(chad[i]+ "\n")
	g.close()


	# work for dates.txt
def create_dates(init_data):
	date_list = []
	date = []
	rows = []

	for line in init_data:
		m = line.index("<date>")
		n = line.index("</date>")
		c = line.index("<row>")
		u = line.index("</row>")
		
		date.append(line[m+6:n])
		rows.append(line[c+5:u])

	for i in range(0,len(date)):
		v = ""
		v = v + date[i] + ":" + rows[i]
		date_list.append(v)
		
	# print(date_list)

	g = open("dates10.txt","w+")

	for i in range(0,len(date_list)):
		g.write(date_list[i]+ "\n")

	g.close()

	# work for recs.txt
def create_records(init_data):
	date = []
	rows = []
	for line in init_data:
		
		m = line.index("<mail>")
		n = line.index("</mail>")
		c = line.index("<row>")
		u = line.index("</row>")  
		
		date.append(line[m:n+7])
		rows.append(line[c+5:u])

	chad = []
	for i in range(0,len(date)):
		v = ""
		v = v + rows[i] + ":" + date[i]  
		chad.append(v)
		

	g = open("recs10.txt","w+")

	for i in range(0,len(chad)):
		g.write(chad[i]+ "\n")  
	
	g.close()


# work for terms.txt
def create_terms(init_data):
	terms_list = []
	body = []
	for test in init_data:
			y = test.index("<mail>")
			er = test.index("</mail>")
			xa = test[y:er].replace("&lt;", "<")
			xa = test[y:er].replace("&gt;", ">")
			xa = test[y:er].replace("&amp;", "&")
			xa = test[y:er].replace("&apos;", "'")
			xa = test[y:er].replace("&quot;", '"')
			terms_list.append(xa)

	for line in terms_list:
		o = line.index("<subj>")
		p = line.index("</subj>")
		m = line.index("<body>")
		n = line.index("</body>")
		c = line.index("<row>")
		u = line.index("</row>") 
		
		emp = line[o+6:p].lower()
		'''
		emp = emp.replace("&#10;"," ")
		emp = emp.replace(",", " ")
		emp = emp.replace(":", " ")
		emp = emp.replace(".", " ")
		emp = emp.replace("/"," ")
		emp = emp.replace("&"," ")
		emp = emp.replace("'"," ")
		emp = emp.replace('"'," ")
		'''

		emp = emp.replace("&apos;"," ")
		emp = emp.replace("&amp;"," ")
		emp = emp.replace("&#10;"," ")
		emp = emp.replace("?"," ")
		emp = emp.replace("!"," ")
		emp = emp.replace(",", " ")
		emp = emp.replace(":", " ")
		emp = emp.replace(".", " ")
		emp = emp.replace("/"," ")
		emp = emp.replace("\\"," ")
		emp = emp.replace("~"," ")
		emp = emp.replace("&"," ")
		emp = emp.replace("("," ")
		emp = emp.replace(")"," ")
		emp = emp.replace("+"," ")
		emp = emp.replace("="," ")
		emp = emp.replace("*"," ")
		emp = emp.replace("["," ")
		emp = emp.replace("]"," ")
		emp = emp.replace("@"," ")
		emp = emp.replace("<"," ")
		emp = emp.replace(">"," ")
		emp = emp.replace("$"," ")
		emp = emp.replace("%"," ")
		emp = emp.replace("^"," ")
		emp = emp.replace("}"," ")
		emp = emp.replace("{"," ")
		emp = emp.replace("#"," ")
		emp = emp.replace(";"," ")
		emp = emp.replace("`"," ")
		emp = emp.replace("'"," ")
		emp = emp.replace('"'," ")
		emp = emp.split()

		#subj part  
		for v in emp:
			#v[0] != '&' and
			if v != "" and len(v) > 2:
				body.append("s-" + v + ":" + line[c+5:u])
				
		emp = line[m+6:n].lower()
		emp = emp.replace("&apos;"," ")
		emp = emp.replace("&amp;"," ")
		emp = emp.replace("&#10;"," ")
		emp = emp.replace("?"," ")
		emp = emp.replace("!"," ")
		emp = emp.replace(",", " ")
		emp = emp.replace(":", " ")
		emp = emp.replace(".", " ")
		emp = emp.replace("/"," ")
		emp = emp.replace("\\"," ")
		emp = emp.replace("&"," ")
		emp = emp.replace("("," ")
		emp = emp.replace("~"," ")
		emp = emp.replace(")"," ")
		emp = emp.replace("+"," ")
		emp = emp.replace("="," ")
		emp = emp.replace("*"," ")
		emp = emp.replace("["," ")
		emp = emp.replace("]"," ")
		emp = emp.replace("@"," ")
		emp = emp.replace("<"," ")
		emp = emp.replace(">"," ")
		emp = emp.replace("$"," ")
		emp = emp.replace("%"," ")
		emp = emp.replace("|"," ")
		emp = emp.replace("^"," ")
		emp = emp.replace("}"," ")
		emp = emp.replace("{"," ")
		emp = emp.replace("#"," ")
		emp = emp.replace(";"," ")
		emp = emp.replace("`"," ")
		emp = emp.replace("'"," ")
		emp = emp.replace('"'," ")

		emp = emp.split()
		for x in emp:
			if x != "" and len(x) > 2:
				body.append("b-" + x  + ":" + line[c+5:u])
				
	g = open("1k-output.txt","w+")
				
	for i in range(0,len(body)):
		g.write(body[i]+ "\n")

	g.close()
main()
