from login import login
def main():
	print("Hi! This is a Coverage Automation System. It will:\n1. Take in a CSV File of Addresses\n2. Check the coverage of the addresses\n3. Output a \'Y\' or \'N\' depending on the existence of coverage.")
	path_to_csv = input("Please ensure you have a 'partners_coveragecheck.csv' file in the same directory. Type 'Y' to confirm.")
	login('DPSL9701', 'Djns513!!')
	# print("Would you like the coverage test to match the ones given in the table?")
	# print("1. Only for the addresses without Building Name.") # will not work. because the addresses with building names might require further uni no specified as well.
	# print("2. Yes - match for all the addresses.")
	# print("3. No - do not match for all the addresses.")

if __name__ == '__main__':
	main()


