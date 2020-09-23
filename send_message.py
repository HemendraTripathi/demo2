import requests,json,sqlite3,telegram
def send_message(TOKEN):
	bot = telegram.Bot(TOKEN)
	try:
		with open('chat_id','r') as a:
			chat_id = int(a.readline())
			a.close()
	except FileNotFoundError:
		print("'chat_id' file not found! retry...\nTry Sending your Password to Bot and check after few seconds. ")
		exit(10)
	try:
		db_filename = open('data','r')
	except FileNotFoundError:
		print("'data' file not found!")
		exit(11)
		
	name = db_filename.readline()
	db_filename.close()
	conn = sqlite3.connect(name)
	c = conn.cursor()
	try:
		c.execute("SELECT * FROM receive")
		rec_addr = c.fetchall()
		c.execute("SELECT * FROM send")
		sen_addr  =c.fetchall()
	except sqlite3.OperationalError:
		print("DataBase Error!")
		exit(12)
		
	for i in range(len(rec_addr)):

		conn = sqlite3.connect(name)
		c = conn.cursor()
		try:
			c.execute("SELECT * FROM send")
			sen_addr = c.fetchall()
		except sqlite3.OperationalError:
			print("DataBase Error!")
			exit(13)
		
		if len(sen_addr) == 0:
			order_no = 1000
			
		else:
			temp = sqlite3.connect(name)
			cu = temp.cursor()
			try:
				cu.execute("SELECT * FROM send")
				sen = cu.fetchall()
				#print(sen[-1][5])
				order_no = sen[-1][6] + 1
				temp.close()
			except sqlite3.OperationalError:
				print("DataBase Error!")
				exit(14)
		a = str(sen_addr)
		if rec_addr[i][1] in a:
			continue
		else:	
			to_put = rec_addr[i]
			to_put = list(to_put)
			to_put.append(order_no)
			to_put.append("pending")
			#to_put.append(0)
			to_put = tuple(to_put)
			
			text = "*************\nOrder No. : "+str(order_no)+"\nAddress : "+rec_addr[i][2]+"\nGroup : "+rec_addr[i][4]+"\nUser : "+rec_addr[i][3]+"\nTime : "+rec_addr[i][1]+"\nDate : "+rec_addr[i][0]+"\nApproval : Pending"+"\n*************"
			
			buttons = [[telegram.InlineKeyboardButton("Approve",callback_data="--approve"),telegram.InlineKeyboardButton("Disapprove",callback_data="--disapprove"),telegram.InlineKeyboardButton("Cancel",callback_data="--cancel")]]
			
			reply_markup = telegram.InlineKeyboardMarkup(buttons)
			bot.send_message(chat_id=chat_id,text=text,reply_markup=reply_markup)
			print("\nSend Message :- "+text+"\n")
			#url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
			#print(url)
			#try:
			#	x = requests.get(url)
			#except requests.exceptions.ConnectionError:
			#	print("Check Your Internet Connection !")
			#	exit(15)

			#y = json.loads(x.text)
			#if y['ok']:	
			c.execute("INSERT INTO send (date,time,address,user_name,group_name,user_chat_id,order_no,approval) VALUES(?,?,?,?,?,?,?,?)",to_put)
			order_no += 1
			conn.commit()
			conn.close()
		#write this y to database table send_message			
	conn.close()

