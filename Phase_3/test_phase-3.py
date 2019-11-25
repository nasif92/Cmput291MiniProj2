from bsddb3 import db
from datetime import *
import re


# a small UI design for the starting user screen
def main():
	
	print(
'''
Welcome to Our program
As you might know already, we are using Berkeley db

So this is the set of input types we can take with any of our index files

1.  subj:gas
2.  subj:gas body:earning
3.  confidential%
4.  from:phillip.allen@enron.com
5.  to:phillip.allen@enron.com
6.  to:kenneth.shulklapper@enron.com  to:keith.holst@enron.com
7.  date:2001/03/15
8.  date>2001/03/10
9.  bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com
10. body:stock  confidential  shares  date<2001/04/12
''')

	exit_prog = False
	# prompt for input type 
	while not exit_prog:
		o_type = input (
	'''Put your query here. Type q to quit: ''')
		# exit program only if q is pressed
		if o_type.lower() == "q":
			print()
			exit_prog = True
			print("Exiting. GoodBye!")
		else:
			break_user_input(o_type)


# breaks the user input into specific queries
def break_user_input(user_input):
	# taking into fact that if there is a colon that doesn't separate the stuff
	headers = [":",">","<"]
	ca = user_input.split(" ")
	while "" in ca:
		ca.remove("")
	for header in headers:
		for query in ca:
			if header in query:
				if len(query) == 1:
					i = ca.index(header)
					ca[i-1:i+2] = ["".join(ca[i-1:i+2])]
				else:
					i = query.index(header)
					list_index = ca.index(query)
					if i == 0:
						ca[list_index-1:list_index+1] = ["".join(ca[list_index-1:list_index+1])]
					elif i == len(query) - 1:
						ca[list_index] = ca[list_index] + ca[list_index + 1]
						del ca[list_index + 1]

	output_type = "brief"
	if "=" in ca[0]:
		output_type = ca[0][ca[0].index("=") : len(ca[0])]
		if output_type == "brief":
			print("In brief mode")
		elif output_type == "full":
			print("In full mode")
	else:
		query_type = check_query_type(ca)
		print(ca, query_type, output_type)
		process_query(ca, query_type, output_type)




# this function should check the type of the query 
def check_query_type(queries):
	query_type = []
	for query in queries:
		print(query)
		if ":" in query:
			query_type.append(query[0:query.index(":")])
		elif "<" in query or ">" in query:
			query_type.append("date")
		elif "=" in query:
			query_type.append("output")
		else:
			query_type.append("terms")
	
	email_prefix = ["from" , "to" , "cc" , "bcc"]
	i = 0
	for query in query_type:
		print(query)
		if query != "sub":
			for email in email_prefix:
				if email in query:
					query_type[i] = "emails"
		elif query == "sub":
			query_type[i] = "terms"
		elif query != "date"and query != "terms" and query != "emails":
			query_type[i] = None
		i+=1
	return query_type

# a function which takes in the queries and calls the other functions for query output
def process_query(queries, query_types,output_type):
	final = set()
	query_type = query_types[0]
	if query_type == "date":
		for v in getDate(queries[query_types.index(query_type)]).values():
			final.add(v)
	elif query_type == "emails":
		for v in getEmail(queries[query_types.index(query_type)]).keys():
			print("First step: " + str(v))
			final.add(v)
	if query_type == "terms":
		for v in getTerms(queries[query_types.index(query_type)]).values():
			final.add(v)
	
	if len(queries) > 1:
		size = len(queries)
		i = 1
		
		while(i < size):
			a_set = set()
			if query_type == "date":
				for v in getDate(queries[i]).values():
					a_set.add(v)
					final = final.intersection(a_set)
			elif query_type == "emails":
				for v in getEmail(queries[i]).keys():
					a_set.add(v)
					print(final, a_set)
					final = final.intersection(a_set)
			elif query_type == "terms":
				for v in getTerms(queries[i]).values():
					a_set.add(v)
					final = final.intersection(a_set)
			i+=1
	if len(final) == 0:
		print("No output found in the index files")
	else:
	# after everything is found we open the database
		DB_File = "re.idx"
		database = db.DB()
		database.set_flags(db.DB_DUP)
		database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
		curs = database.cursor()
		dictionary = {}
		for x in final:
			dictionary[x] = "final"
		for key in dictionary.keys():
			query = curs.set(key.encode("utf-8")) 
			if(query != None):
				mail = query[1].decode("utf-8")
				a = mail.index("<subj>")
				b = mail.index("</subj>")
				sub = mail[a+6:b]
				if len(sub) == 0:
					sub = "No subject"
				print("Row : " + key + " Subject: " + sub)
				
				dup = curs.next_dup()
				while(dup != None):
					dup = curs.next_dup()
			else:
				print("No Entry Found.")
        

# the specific queries bruh
def getDate(query):
	DB_File = "da.idx"
	database = db.DB() #handle for Berkeley DB database
	database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
	curs = database.cursor()
	iter = curs.first()
	DB_File = "da.idx"
	database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
	curs = database.cursor()
	iter = curs.first()
	headers = [":","<",">"]
	test = {}
	for header in headers:
		if header in query:
			year,month,day = query[query.index(header) + 1: len(query)].split("/")
			print(int(year),int(month),int(day))
			term_date = datetime(int(year),int(month),int(day))
			prefix = header
	while iter:
		date_to_compare = iter[0].decode().split("/")
		year2 = int(date_to_compare[0])
		month2 = int(date_to_compare[1])
		day2 = int(date_to_compare[2])
		other_date = datetime(year2,month2,day2)
		if prefix == ":":
			if other_date == term_date:
				test[iter[1].decode()] = iter[0].decode()
		elif prefix == ">":
			if other_date > term_date:
				test[iter[1].decode()] = iter[0].decode()
		elif prefix == ">=":
			if other_date >= term_date:
				test[iter[1].decode()] = iter[0].decode()
		elif prefix == "<=":
			if other_date <= term_date:
				test[iter[1].decode()] = iter[0].decode()
		elif prefix == "<":
			if other_date < term_date:
				test[iter[1].decode()] = iter[0].decode()
		iter = curs.next()
	return test


def getEmail(query):
	DB_File = "em.idx"
	database = db.DB()
	print("Inside emails")
	database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
	database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
	curs = database.cursor()
	final_dictionary = {}
	query = query.replace(":","-")
	result = curs.set(query.encode("utf-8")) 
	#In the presence of duplicate key values, result will be set on the first data item for the given key. 

	if(result != None):
		final_dictionary[result[1].decode("utf-8")] = str(result[0].decode("utf-8"))            
		dup = curs.next_dup()
		while(dup != None):
			final_dictionary[dup[1].decode("utf-8")] = str(dup[0].decode("utf-8"))
			dup = curs.next_dup()
	curs.close()
	database.close()
	return final_dictionary

def getTerms(query):
	DB_File = "te.idx"
	database = db.DB()

	database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
	curs = database.cursor()
	iter = curs.first()
	test = {}
	term = query
	if term[-1] == "%":
		term = term[:-1]
		while iter:
			term_to_compare = iter[0].decode() # s
			if re.search(r'\b' + term, term_to_compare):
				test[iter[0].decode()] = iter[1].decode()
			iter = curs.next()                
	else:        
		while iter:
			term_to_compare = iter[0].decode() 
			if re.search(r'\b' + term + r'\b', term_to_compare): # THIS GOES TO TE.IDX FILE
				test[iter[0].decode()] = iter[1].decode()
			iter = curs.next()
	return test

main()