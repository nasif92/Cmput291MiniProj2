import datetime, sys
def main():
	a = datetime.datetime.now()
	file = sys.argv[1]
	if file == "":
		print("No file given or present")
	else:
		f = open(file,"r")

		init_data = []
			
		for line in f:
			init_data.append(line)

		# each function is passed in the init data from the file
		create_emails(init_data)
		create_terms(init_data)
		create_records(init_data)
		create_dates(init_data)
		f.close()
		b = datetime.datetime.now()
		print("Total time required: %s" %(b-a))


def create_emails(init_data):
	# work for emails.txt
	
	email_list = []

	del init_data[0], init_data[0], init_data[-1]

	for test in init_data:
		y = test.index("<mail>")
		er = test.index("</mail>")
		email_list.append(test[y:er])
		
	g = open("emails.txt","w+")

	for testy in email_list:
		m = testy.index("<from>")
		n = testy.index("</from>")
		t_o = testy.find("<to>")
		t_p = testy.find("</to>")
		c = testy.index("<row>")
		u = testy.index("</row>")
		cc = testy.find("<cc>")
		cc_end = testy.find("</cc>")
		bcc = testy.find("<bcc>")
		bcc_end = testy.find("</bcc>")

		row_num = testy[c+5:u]
		g.write("from-" + testy[m+6:n] +":"  +  row_num + "\n")
		
		# for to
		to = testy[t_o+4:t_p].split(',')
		to_str = ""
		for x in to:
			if x != "":
				to_str +=  "to-" + x  + ":"  + row_num + "\n"
		g.write(to_str)

		# for cc
		cc_str = ""
		cc = testy[cc+4:cc_end].split(',')
		for x in cc:
			if x != "":
				cc_str += "cc-" + x + ":" + row_num + "\n"
		g.write(cc_str)

		# for bcc
		bcc_str = ""
		bcc = testy[bcc+5:bcc_end].split(',')
		for x in bcc:
			if x != "":
				bcc_str += "bcc-" + x + ":" + row_num + "\n"
		g.write(bcc_str)

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
		

	g = open("dates.txt","w+")

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
		

	g = open("recs.txt","w+")

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
				
	g = open("terms.txt","w+")
				
	for i in range(0,len(body) ):
		g.write(body[i]+ "\n")
	g.close()
main()