from bsddb3 import db
import re
from datetime import *

# breaks the user input into specific queries
def break_user_input(user_input):
    # taking into fact that if there is a colon that doesn't separate the stuff
    ca = user_input.split(" ")
    headers = [":","<",">"]
    while "" in ca:
        ca.remove("")

    for query in ca:
	    for header in headers:
		    if header in query:
			    if len(query) == 1:
				    i = ca.index(header)
				    ca[i-1:i+2] = ["".join(ca[i-1:i+2])]
    for query in ca:
    	pos = 0
    	for header in headers:
    		if header in query and len(query) > 1:
    			if query.index(header) == 0:
    				pos = ca.index(query)
    				ca[pos-1] = ca[pos-1] + ca[pos]
    				ca[pos] = ""
    			elif query.index(header) == len(query) -1:
    				pos = ca.index(query)
    				ca[pos] = ca[pos] + ca[pos + 1]
    				ca[pos + 1] = ""
	
    while "" in ca:
        ca.remove("")
				
    return ca


def check_validity(query):
    # Here is where we check if the query is valid
    
    # Is it a date? we check here with an emphasis on split.
    datetype = [':' , '>=' , '<=', '>' , '<']
    chosen = ''
    for typ in datetype:
        datePrefix = query.split(typ)
        if len(datePrefix) == 2:
            chosen = typ
            if datePrefix[0] == 'date':
                checkdate = datePrefix[1].split('/') # We check the actual date itself
                if len(checkdate) == 3:
                    for i in checkdate:
                        if not i.isdigit(): # We check each segment of the date to be digits (restrictions on month and day need to be applied)
                            return None
                        elif int(checkdate[1]) < 1 or int(checkdate[1]) > 12 or int(checkdate[2]) < 1 or int(checkdate[2]) > 31:
                            return None
                    return "datequery"
            
                

 
    email_prefix = ['from' , 'to' , 'cc' , 'bcc']  #If the query is not a date, we check it to see if it is possibly an email.
    email = query.split(":")
    if len(email) == 2: # We see if splitting it causes a length of 2, then check the prefix
        for prefix in email_prefix:
            if email[0] == prefix: 
                check_email_terms = email[1].split("@") # Split it again for the email term
                if len(check_email_terms) == 2: # Checks to see if there is a right term and left term.
                    left_side = check_email_terms[0].split('.')
                    right_side = check_email_terms[1].split('.') # Split on period to check for alphanumericals.
                    if len(left_side) > 0:
                        for string in left_side:
                            string = string.replace("-","")
                            string = string.replace("_","")
                            if not string.isalnum():
                                return None
                    if len(right_side) > 0:
                        for string in right_side:
                            string = string.replace("-","")
                            string = string.replace("_","")
                            if not string.isalnum():
                                return None
                    return "emailquery"
                return None
                
    term_prefix = ["subj" , "body"] # If not email, check for term.
    term = query.split(":")
    if len(term) == 2: # Split and check like before
        for prefix in term_prefix:
            if term[0] == prefix:
                if term[1][-1] == "%" or term[1][-1].isalnum():
                    return "termquery"
                else: 
                    return None
    elif len(term) == 1:
                term_string = query[-1]
                if term_string == "%" and query[0:len(query)-1].isalnum() or query.isalnum():
                    return "termquery" 
                
    #By default, the output of each query is the row id and the subject field of all matching emails. 
    check_mode = query.split("=")
    if len(check_mode) == 2:
        if check_mode[0] == "output":
            if check_mode[1] == "full":
                return "printinfull"
            elif check_mode[1] == "brief":
                return "printbriefly"
            else:
                return None

# this function puts the correct prefixes for the queries for moving to the next phase      
def process_query(query,Type):
    
    if Type == "termquery":
        segment = query.split(":")
        if len(segment) == 2:
            prefix = segment[0]
            address = segment[1]
            if prefix == "subj":
                return "s-", address
            else:
                return "b-", address
        else:
            return "",query
    
    if Type == "emailquery":
        segment = query.split(":")
        prefix = segment[0]
        address = segment[1]
        return prefix, address
    
    if Type == "datequery":
        datetype = [':' , '>=' , '<=', '>' , '<']
        chosen = ''
        for typ in datetype:
            datePrefix = query.split(typ)
            if len(datePrefix) == 2:
                chosen = typ
                return chosen, datePrefix[1] 

# OPENS UP IDX FILES AND GETS ANY MATCHES AND PRINTS IT OUT    
def query_test(prefix, term, output):   
    datetype = [':' , '>=' , '<=', '>' , '<']
    for typ in datetype:
        if prefix == typ:  
            split = term.split("/")
            year = int(split[0])
            month = int(split[1])
            day = int(split[2])
            term_date = datetime(year, month, day)
            database = db.DB() #handle for Berkeley DB database
            test = {}
            DB_File = "da.idx"
            database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
            curs = database.cursor()
            iter = curs.first() 
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

    if prefix == "s-" or prefix == "b-" or prefix == "":
        database = db.DB() #handle for Berkeley DB database
        test = {}
        
        DB_File = "te.idx"
        database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
        curs = database.cursor()
        iter = curs.first()
        if term[-1] == "%":
            term = term[:-1]
            while iter:
                term_to_compare = iter[0].decode() # s
                if re.search(r'\b' + term, term_to_compare) and prefix in term_to_compare[0:2]:
                    test[iter[0].decode()] = iter[1].decode()
                iter = curs.next()                
        else:        
            while iter:
                term_to_compare = iter[0].decode() 
                if re.search(r'\b' + term + r'\b', term_to_compare) and prefix in term_to_compare[0:2]: # THIS GOES TO TE.IDX FILE
                    test[iter[0].decode()] = iter[1].decode()
                iter = curs.next()

    # this part works for checking emails           
    elif prefix == "from" or prefix == "to" or prefix == "bcc" or prefix == "cc":
        database = db.DB() #handle for Berkeley DB database
        test = {}
        DB_File = "em.idx"
        database.open(DB_File ,None, db.DB_BTREE, db.DB_CREATE)
        curs = database.cursor()
        iter = curs.first()  
        while iter:
            term_to_compare = iter[0].decode()   
            if re.search(r'\b' + term, term_to_compare) and prefix in term_to_compare[0:5]:
                test[iter[1].decode()] = iter[0].decode()
            iter = curs.next()
            
    
    vs = []
    curs.close()
    database.close()  
    database = db.DB()
    DB_File = "re.idx"
    database.open(DB_File ,None, db.DB_HASH, db.DB_CREATE)    
    curs = database.cursor()
    
    # if output type is brief, check the required prefixes and generate the row id's
    if output == "printbriefly":           
        for value in test:
            iter = curs.first()   
            while iter:
                if prefix == "s-" or prefix == "b-" or prefix == "":
                    if int(iter[0].decode()) == int(test.get(value)):
                        list_pair = {}
                        o = iter[1].decode().index("<subj>")
                        p = iter[1].decode().index("</subj>")                
                        subject_body = iter[1].decode()[o+6:p]
                        if len(subject_body) == 0:
                            list_pair[test.get(value)] = "No Subject Given"
                        else:
                            list_pair[test.get(value)] = iter[1].decode()[o+6:p]                    
                        vs.append(list_pair)
                elif prefix == "from" or prefix == "to" or prefix == "bcc" or prefix == "cc":
                    if int(iter[0].decode()) == int(value):
                        list_pair = {}
                        o = iter[1].decode().index("<subj>")
                        p = iter[1].decode().index("</subj>") 
                        subject_body = iter[1].decode()[o+6:p]
                        if len(subject_body) == 0:
                            list_pair[value] = "No Subject Given"
                        else:
                            list_pair[value] = iter[1].decode()[o+6:p]
                        vs.append(list_pair)
                iter = curs.next()
                   
            for typ in datetype:
                if prefix == typ:
                    iter = curs.first()     
                    while iter:
                        list_pair = {}
                        if int(iter[0].decode()) == int(value):
                            o = iter[1].decode().index("<subj>")
                            p = iter[1].decode().index("</subj>") 
                            subject_body = iter[1].decode()[o+6:p]
                            if len(subject_body) == 0:
                                list_pair[value] = "No Subject Given"
                            else:
                                list_pair[value] = iter[1].decode()[o+6:p]
                            vs.append(list_pair)
                        iter = curs.next()           
        
                    
    else:
        for value in test:
            iter = curs.first()   
            while iter:
                if prefix == "s-" or prefix == "b-" or prefix == "":
                    if int(iter[0].decode()) == int(test.get(value)):
                        list_pair = {}
                        subject_body = iter[1].decode()
                        list_pair[test.get(value)] = iter[1].decode()                   
                        vs.append(list_pair)
                elif prefix == "from" or prefix == "to" or prefix == "bcc" or prefix == "cc":
                    if int(iter[0].decode()) == int(value):
                        list_pair = {}
                        list_pair = {}
                        subject_body = iter[1].decode()
                        list_pair[value] = iter[1].decode()
                        vs.append(list_pair)
                iter = curs.next()
                   
            for typ in datetype:
                if prefix == typ:
                    iter = curs.first()     
                    while iter:
                        list_pair = {}
                        if int(iter[0].decode()) == int(value):
                            list_pair = {}
                        subject_body = iter[1].decode()
                        list_pair[test.get(value)] = iter[1].decode()                   
                        vs.append(list_pair)
                        iter = curs.next()     
                        
    return vs
              
    
# works for multiple queries 
def multi_query(mq,output):
    sq = mq[0]
    first_set = {1}
    first_set.remove(1)
    for test in sq:
        for cs in test:
            first_set.add(cs)
    
    for each_query in mq:
        set_to_compare = {1}
        set_to_compare.remove(1)
        for eac in each_query:
            for key in eac:
                set_to_compare.add(key)
        first_set = first_set & set_to_compare
        
    for i in range(0,50):
        print("=", end="")
    print("")  
    if output == "printbriefly":
        for val in first_set:
            for key in sq:
                for keys in key:
                    if val == keys:
                        print("Row ID: #" + keys + ", Subject: " +  key[keys])
        
        for i in range(0,50):
            print("=", end="")
        print("")     
    
    else:
        for val in first_set:
            for key in sq:
                for keys in key:
                    if val == keys:
                        print( "Full Unparsed Record for Row ID # " + keys + ": "+  key[keys])        
        
        for i in range(0,50):
            print("=", end="")
        print("")        
    
       
        
def main():
    # Setting up the loop and output to default brief here.
    loop = True
    output_type = "printbriefly"
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

    while loop:
        
        all_query_result = []   # The list that will contain seperate results of all individual queries
        allow_query = True  # To check if any syntax has been violated.
        user_input = str(input("Enter !q! to exit, otherwise enter a valid query: "))
        user_input = user_input.lower()
        if user_input == '!q!':
            loop = False
            print("Exiting Program....")
        else:
            user_queries = break_user_input(user_input) # If user enters queries with extra spacing, it is handled here.
            query_type = [] # List containing the types of queries we get from the input
            
            for i in user_queries: #For each query inputted, we check to see if it follows the syntax via check_validity function.
                
                query_type.append(check_validity(i.lower()))
                # query type is only going to append if it's a va;id query
            
            
            for i in query_type:    
                if i == None:
                    print("One of the queries are invalid, please try again")
                    allow_query = False
                if (i == "printbriefly" or i == "printinfull") and len(query_type) > 1:
                    print("When changing output, do not do any other additional queries. Only do one output change in a line")
                    allow_query = False
                elif i == "printbriefly":
                    output_type = i
                    allow_query = False
                    for i in range(0,50):
                        print("=", end="")
                    print('\nNOTE: You have changed the output to brief.\nYou will only get the row id and subject of any matches.\nEmpty subjects will say that there is "No Subject Given"\nto change to a full output, type in "output=full."')
                    for i in range(0,50):
                        print("=", end="")
                    print("")
                elif i == "printinfull":
                    output_type = i
                    allow_query = False
                    for i in range(0,50):
                        print("=", end="")                    
                    print('\nNOTE: You have changed the output to full.\nYou will get the full UNPARSED record of any matches.\nTo change to a more brief output, type in "output=brief".')
                    for i in range(0,50):
                        print("=", end="")
                    print("")                    
            to_do = []
            if allow_query: #if we didn't specify brief or full in the query
                for i in range(0,len(user_queries)):
                    to_do.append(process_query(user_queries[i], query_type[i]))
                            
                for tupl in to_do:
                    all_query_result.append(query_test(tupl[0],tupl[1], output_type))
                                        
                multi_query(all_query_result,output_type)
            
main()




