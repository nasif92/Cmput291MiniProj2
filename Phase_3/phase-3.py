
# a small UI design for the starting user screen
def main():
	
	print(
'''
Welcome to Our program
As you might know already, we are using Berkeley db
For running the program you have to choose any of the following options
			
1) Choose your own index file
2) Choose one of our index files
''')

	prompt = input("Type  (1/2) : ")
	if prompt is "1":
		filename = input ("Enter index filename: ")
	else:
		print(
'''
Alright!
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
	# prompt for input type if output = full/ output = brief
	o_type = input (
'''Select your output type (full/brief) 
Output-type= ''')
	correct_type = 0
	if o_type == "":
		print("No type given. At default")
	elif o_type.lower() == "brief":
		print("Awesome. Output type is set to brief")
		correct_type = 1
	elif o_type.lower() == "full":
		print("Awesome. Output type is set to full")
		correct_type = 2
	else:
		print("Output type is wrong")
	
	# type 1 and 2 is here
	if correct_type == 1:
		print("Brief")

	# for type 1





	elif correct_type == 2:
		print("Descriptive")

	# for type2

main()