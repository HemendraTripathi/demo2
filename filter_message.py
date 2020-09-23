import re,datetime,sqlite3
def filter_message(message,user_name,date,group_name,user_chat_id):
	#print("***********\nIN FILTER \n**********")
	temp_date = date
	try:
		db = open('data','r')
		db_filename = db.readline()
		db.close()
	except FileNotFoundError:
		print("'data' file not found!")
		exit(7)
		
	date = datetime.datetime.fromtimestamp(date).strftime("%c")
	time = datetime.datetime.fromtimestamp(temp_date).strftime("%H:%M:%S")
	date = date.replace(time,'')
	address = message
	if address.startswith('/'):
		print('Oops!, Not a Valid Message.')
	else:
		data = []
		if len(address) > 0:
			#print(f"Address : {address} , Date : {date} , Group Name : {group_name} , User : {user_name}")
			conn = sqlite3.connect(db_filename)
			c = conn.cursor()
			data.append(date)
			data.append(time)
			data.append(address)
			data.append(user_name)
			data.append(group_name)
			data.append(user_chat_id)
			data = tuple(data)
			#print(data)
			try:
				c.execute("SELECT * FROM receive")
			except sqlite3.OperationalError:
				print("DataBase Error!")
				exit(8)
			emai = c.fetchall()
			if data in emai:
				print('Already Satisfied')
			else:
				try:
					c.execute("INSERT INTO receive (date,time,address,user_name,group_name,user_chat_id) VALUES (?,?,?,?,?,?)",data)
				except sqlite3.OperationalError:
					print("DataBase Error!")
					exit(9)
					
			conn.commit()
			conn.close()
