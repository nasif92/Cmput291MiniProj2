from bsddb3 import db

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
						ca[list_index:list_index+2] = ["".join(ca[list_index:list_index+2])]
	output_type = "brief"
	if "=" in ca[0]:
		output_type = ca[0][ca[0].index("=") : len(ca[0])]
		if output_type == "brief":
			print("In brief mode")
		elif output_type == "full":
			print("In full mode")
	else:
		query_type = check_query_type(ca)
		process_query(ca, query_type, output_type)




# this function should check the type of the query 
def check_query_type(queries):
	query_type = []
	for query in queries:
		if ":" in query:
			query_type.append(query[0:query.index(":")])
		elif "<" in query or ">" in query:
			query_type.append("date")
		elif "=" in query:
			query_type.append("output")
		else:
			query_type.append("terms")
	
	email_prefix = ["from" , "to" , "cc" , "bcc"]
	for query in query_type:
		print(query)
		if query != "terms":
			for emails in email_prefix:
				if emails == query and "sub" not in query:
					query_type[query_type.index(query)] = "emails"
		elif "sub" in query:
			query_type[query_type.index(query)] = "terms"
		if query != "date" and query != "sub" and query != "terms" and query != "emails":
			query_type[query_type.index(query)] = None

	return query_type
# a function which takes in the queries and calls the other functions for query output
def process_query(queries, query_types,output_type):
	final_dictionary = {}
	for query_type in query_types:
		if query_type == "date":
			final_dictionary [getDate(queries[query_types.index[query_type]]) ]
		elif query_type == "email":
			final_dictionary [getEmail(queries[query_types.index[query_type]])]
		elif query_type == "terms":
			final_dictionary[getTerms(queries[query_types.index[query_type]])]
		else:
			print("No output")

# the specific queries bruh
def getDate(query):
	DB_File = "da.idx"
	database = db.DB() #handle for Berkeley DB database
	database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
	curs = database.cursor()
	iter = curs.first()
	
def getEmail(query):
	pass
def getTerms(query):
	pass

main()