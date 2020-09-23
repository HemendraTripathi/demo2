import requests,json,sqlite3,telegram,re
from filter_message import filter_message
from google_map import google_autocomplete

def get_message(TOKEN,API_TOKEN,WEBHOOK_MESSAGE):
	#response function to check if message already responded
	def response(message,user,date):
		some_list = (message,user,date)
		try:
			db = open('data','r')
			db_filename = db.readline()
			db.close()
			
		except FileNotFoundError:
			print("'data' file not found!")
			exit(37)
		try:
			conn = sqlite3.connect(db_filename)
			c = conn.cursor()
			c.execute("SELECT * FROM response")
			temp_list = c.fetchall()
			for item in temp_list:
				if message in item:
					if user in item:
						if date in item:
							return True
							break
						else:
							continue
					else:
						continue
				else:
					continue
			c.execute("INSERT INTO response (message,user,date) VALUES (?,?,?)",some_list)
			conn.commit()
			conn.close()
			return False
			
		except sqlite3.OperationalError:
			print("DataBase Error!")
			exit(39)
	
	#defining bot
	bot = telegram.Bot(TOKEN)
	approval_flag = False
	suggestion_flag = False


	flag = False
	error_flag =True
	try:#get username also
		#normal message
		message_type = WEBHOOK_MESSAGE['message']['chat']['type']
		user_name = ""
	except KeyError:
		try:#callback message
			message_type = WEBHOOK_MESSAGE['callback_query']['message']['chat']['type']
			user_name = ""
			approval_flag = True
			suggestion_flag = True
		except KeyError:
			print("Some Callback Error!")
	if message_type == "private" and approval_flag == False:
		try:
			text = WEBHOOK_MESSAGE['message']['text']
			if text == "/start_password":#add username for extra security
				chat_id = WEBHOOK_MESSAGE['message']['from']['id']
				with open("chat_id","w") as temp:
					temp.write(str(chat_id))#write username also
					temp.close()
					return
			else:
				return
		
		except KeyError:
			print("No Message, going forward...1 ")	
	
	#callback message for approval code
	#-------------------------------------------
	
	elif message_type == 'private' and approval_flag == True:
		message = WEBHOOK_MESSAGE['callback_query']['message']['text']	
		data = WEBHOOK_MESSAGE['callback_query']['data']
		order_no = message.split('\n')[1]
		address  = message.split('\n')[2]
		order_no = int(order_no.split(': ')[1])
		callback_id = WEBHOOK_MESSAGE['callback_query']['id']
		check = ['--approve','--disapprove','--cancel']
		if data in check:
			try:
				with open('data','r') as db:
					name = db.readline()
					db.close()
			except FileNotFoundError:
				print("DataBase Error!")
				exit(21)
			try:
				with open('chat_id','r') as ch:
					chat_id = ch.readline()
					ch.close()
			except FileNotFoundError:
				print("Chat ID not found Error!")
				exit(22)						
			data_list = [data,order_no,callback_id]
			conn = sqlite3.connect(name)
			c = conn.cursor()
			c.execute("SELECT * FROM callback_id")
			temp_call = c.fetchall()
			change = False
			if (callback_id,) in temp_call:
				print("Already Exists.")
				return
			else:
				c.execute("SELECT * FROM send")
				temp_s = c.fetchall()
				for item in temp_s:	
					print("In step 1")
					if data_list[1] in item:
						if data_list[0] in item:
							print(data_list)
							print("No Change Required.")
							change = False
						else:
							item = item
							change = True
							print("Change Required.")
							break
					else:	
						continue

			if change == True:
				temp = list(item)
				user_chat_id = temp[5]
				user_name = temp[3]
				if data_list[0] == '--approve':
					clear_data = 'Approved'
				elif data_list[0] == '--disapprove':
					clear_data = "Disapproved"
				elif data_list[0] == '--cancel':
					clear_data = "Cancelled"
				else:
					clear_data = "Pending"	
			
				c.execute("DELETE FROM send WHERE order_no=?",(data_list[1],))
				conn.commit()
				temp[6] = data_list[1]
				temp[7] = data_list[0]
				#temp[8] = data_list[2]
				temp = tuple(temp)
				#print(temp)
				#print(data_list)
				c.execute("INSERT INTO callback_id (callback_id) VALUES (?)",(data_list[2],))
				c.execute("INSERT INTO send (date,time,address,user_name,group_name,user_chat_id,order_no,approval) VALUES(?,?,?,?,?,?,?,?)",temp)
				conn.commit()
				user_message = f"**********\nDear, {user_name}\n{address}\nOrder No. {data_list[1]}\nYour order is {clear_data}.\n**********"
				bot.send_message(chat_id=user_chat_id,text=user_message)
				conn.close()
				text = "************\nOrder No. : "+str(data_list[1])+"\nApproval : "+data_list[0]+"\n***********"
				bot.send_message(chat_id=chat_id,text=text)
					#else:
					#	continue
		else:
			print("No CallBack...")
			conn.close()
			return
	#----------------------------------
	#Code for suggestion callback
	#-------------------------------
	elif message_type == "group" and suggestion_flag == True:
		force_check = False
		try:			
			callback_id = WEBHOOK_MESSAGE['callback_query']['id']
		except KeyError:
			print("Some Key Error!")
			return
		try:
			with open('data','r') as db:
				name = db.readline()
				db.close()
		except FileNotFoundError:
			print("DataBase Error!")
			exit(51)	
		conn = sqlite3.connect(name)
		c = conn.cursor()
		c.execute("SELECT * FROM callback_id")
		temp_call = c.fetchall()
		conn.close()
		if (callback_id,) in temp_call:
			print("Already Exists.")
			return
			
		message = WEBHOOK_MESSAGE['callback_query']['message']['text']
		data = callback_id = WEBHOOK_MESSAGE['callback_query']['data']
		from_user = WEBHOOK_MESSAGE['callback_query']['from']['first_name']
		try:
			user_name = message.split("\n")[1]
			uu = user_name.split(' ')[1]
			user_name = uu.replace(',','')
		except IndexError:
			#print("Force Check")
			force_check = True	
			user_name = from_user
		date = WEBHOOK_MESSAGE['callback_query']['message']['date']
		group_name = WEBHOOK_MESSAGE['callback_query']['message']['chat']['title']
		chat_id = WEBHOOK_MESSAGE['callback_query']['message']['chat']['id']
		responsed = response(message,from_user,date)
		if responsed == True:
			return
		if user_name == from_user:
			print(data,user_name,date,group_name,chat_id)
			filter_message(data,user_name,date,group_name,chat_id)
			conn = sqlite3.connect(name)
			c = conn.cursor()
			c.execute("INSERT INTO callback_id (callback_id) VALUES(?)",(callback_id,))
			conn.commit()
			conn.close()
			accept_message = "*********\nDear, "+user_name+"\nAddress : "+data+"\nAddress is Verified.\n*********"
			bot.send_message(chat_id = chat_id,text=accept_message)
		else:
			error_msg = f"xxxxxxxx\nOnly, {user_name} can select Address.\nxxxxxxxx"
			bot.send_message(chat_id = chat_id,text=error_msg)
	
		#elif force_check = True:
					
	#----------------------------------

	#message from group
	elif message_type == "group" and suggestion_flag == False:
		#print("11111")
		try:
			#print("2222")
			text = WEBHOOK_MESSAGE['message']['text']
			#print(text)
			if text.startswith('/') and text != "/start_password":
				#print("333")
				#print(text)
				message = text.split('/')[1]
				user_name = WEBHOOK_MESSAGE['message']['from']['first_name']
				chat_id = WEBHOOK_MESSAGE['message']['chat']['id']
				

				
				date = WEBHOOK_MESSAGE['message']['date']
				group_name = WEBHOOK_MESSAGE['message']['chat']['title']
				

					
				error_message = "**********\nDear, "+user_name+", \nAddress : "+message+"\nPlease enter valid Address."+"\n**********"
				accept_message = "*********\nDear, "+user_name+"\nAddress : "+message+"\nAddress is Verified.\n*********"
				

				try:
					db = open('data','r')
					db_filename = db.readline()
					db.close()
					
				except FileNotFoundError:
					print("'data' file not found!")
					exit(37)
				try:
					google = sqlite3.connect(db_filename)
					c = google.cursor()
					c.execute("SELECT * FROM google_addresses")
					google_address_list = c.fetchall()
					google.close()
				except sqlite3.OperationalError:
					print("DataBase Error !")
					exit(40)
				if tuple(message) in google_address_list:
					responsed = response(message,user_name,date)
					if not responsed == True:
						filter_message(message,user_name,date,group_name,chat_id)
						bot.send_message(chat_id=chat_id,text = accept_message)
					#print("++++++++EXIT FILTER+++++++++")
					error_flag = False
					return
				
				#----------------
				else:
					#print("Address Not Found in Previous Database.")
					error_flag = True
						
				#CHANGING THIS CODE
				if error_flag == True:
					#print("In Error Flag")						
					responsed = response(message,user_name,date)
					#print(responsed)
					if responsed == True:
						#print("Continue")
						return
					else:
						print("Not Responded")
						predictions = google_autocomplete(message,API_TOKEN)	
						if predictions[0] == True:
							prediction_message = "**********\nDear, "+user_name+", \nAddress : "+message+"\nTry Suggestions below -"+"\n**********"
							
							force_message = "If you don't see your Address in Above Suggestions Select this - "
							force_button = [[telegram.InlineKeyboardButton(message,callback_data=message)]]
							force_reply_markup = telegram.InlineKeyboardMarkup(force_button)
							
							buttons = []
							google_address = []
							
							for pred in predictions[1]:
								#if pred in google_address_list 
								temp = []
								temp.append(pred)
								temp = tuple(temp)
								if temp in google_address_list:
									#print("Address Already Exist in Google DB.")
									buttons.append([telegram.InlineKeyboardButton(pred,callback_data=pred)])
									continue
								else:
									google_address.append(temp)
									buttons.append([telegram.InlineKeyboardButton(pred,callback_data=pred)])

								
							reply_markup = telegram.InlineKeyboardMarkup(buttons)
							try:
								bot.send_message(chat_id=chat_id,text = prediction_message,reply_markup=reply_markup)
								bot.send_message(chat_id=chat_id,text = force_message,reply_markup=force_reply_markup)
							except telegram.error.BadRequest:
								print("Big Data")
							#bot.send_message(chat_id=chat_id,text = otherwise_msg,reply_markup = other_reply_markup)
							try:
								google = sqlite3.connect(db_filename)
								c = google.cursor()
								#print(pred)
								#print(google_address_list)
								c.executemany("INSERT INTO google_addresses (address) VALUES (?)",google_address)
								google.commit()
								google.close()
								
							except sqlite3.OperationalError:
								print("DataBase Error !")
								exit(45)
						else:
							#print("In error")
							error_button = [[telegram.InlineKeyboardButton(message,callback_data=message)]]
							error_markup = telegram.InlineKeyboardMarkup(error_button)
							bot.send_message(chat_id=chat_id,text = error_message,reply_markup=error_markup)
							#print("send")	
					#-------------------------------------------------------		
				

			else:
				return
				
		except KeyError:
			print("No Message, going forward...2")
		
	else:
		return

		
