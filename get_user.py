import requests,json,sqlite3,os
def get_user(TOKEN):
	try:
		x = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
		y = json.loads(x.text)
		if not y['ok']:
			print("Enter Correct Token!")
			exit(6)
		print(f"""
Response : {y['ok']}
ID : {y['result']['id']}
FirstName : {y['result']['first_name']}
UserName : {y['result']['username']}
		""")
	except requests.exceptions.ConnectionError:
		print("Check Your Internet Connection !")
		exit(4)
	
	if os.path.isfile(str(y['result']['id'])+'.db') :
		print("Database already exists")
	else :
		with open(str(y['result']['id'])+'.db','w') as db:
			db.close()
			print("Database Created.")
			db_filename = str(y['result']['id'])+'.db'
			with open('data','w') as temp:
				temp.write(db_filename)
				temp.close()
			conn = sqlite3.connect(db_filename)
			c = conn.cursor()
			
			c.execute("""CREATE TABLE send (date,time,address,user_name,group_name,user_chat_id,order_no,approval)""")
			c.execute("""CREATE TABLE receive (date,time,address,user_name,group_name,user_chat_id)""")
			c.execute("""CREATE TABLE callback_id (callback_id)""")
			c.execute("CREATE TABLE response (message,user,date)")
			c.execute("CREATE TABLE google_addresses (address)")
			conn.commit()
			conn.close()
