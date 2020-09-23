import shelve,difflib,json
def suggestion(addr_list):
	try:
		a = open('streets.json','r')
		aa = json.load(a)
		streets = aa['streets'][0]
		char = aa['char'][0]
		a.close()
	except FileNotFoundError:
		print("Street File Error!")
		exit(35)
	temp = []
	complete_addresses = []
	for address in addr_list:
		sugg = difflib.get_close_matches(address,streets)
		temp.append(sugg)
	message = ""
	try:
		for i in range(len(addr_list)):
			if len(temp[i]) == 0:
				message += addr_list[i]
			else:
				message += temp[i][0]
				message += " "
	except IndexError:
		pass
	
	for chars in char:
		if chars in message:
			break
		else:
			return [False]
	if len(message) == 0:
		return [False]
	else:
		return [True,message]
