def verify_input(argvs):
	def error():
				print("""
SMART DELIVERY BOT (WITH GOOGLE API).....😃️

  ;)( ;
 :----:     o8Oo./
C|====| ._o8o8o8Oo_.
 |    |  \========/
 `----'   `------'

Enter Tokens
Syntax : python3 app.py TOKEN

	example : python3 app.py af28434:dfsfsf84f44F#$fv43f854f4f
	Or,
	Enter Token
	
Version : 5.1
			""")
				while True:
					TOKEN = input("Enter Telegram Bot Token : ")
					API_TOKEN = input("Enter Google Map API Token : ")
					if len(TOKEN) > 0 and len(API_TOKEN) > 0:
						break
				with open("verify_tel_token","w") as ver_tok:
					ver_tok.write(TOKEN)
					ver_tok.close()
				with open("verify_API_token","w") as ver_tok:
					ver_tok.write(API_TOKEN)
					ver_tok.close()
				return [TOKEN,API_TOKEN]
			
	#token verification
	if len(argvs) == 3:
		with open("verify_tel_token","w") as ver_tok:
			TOKEN = argvs[1]
			ver_tok.write(TOKEN)
			ver_tok.close()
		with open("verify_API_token","w") as ver_tok:
			API_TOKEN = argvs[2]
			ver_tok.write(API_TOKEN)
			ver_tok.close()
		return (True,TOKEN,API_TOKEN)
		
	elif len(argvs) == 1:
		try:
			with open("verify_tel_token","r") as ver_tok:
				TOKEN = ver_tok.readline()
				if TOKEN == "":
					tokens = error()
					print("got it")
					return(True,tokens[0],tokens[1])
			with open("verify_API_token","r") as ver_tok:
				API_TOKEN = ver_tok.readline()
				if API_TOKEN == "":
					tokens = error()
					print("got it")
					return(True,tokens[0],tokens[1])
				else :
					return (True,TOKEN,API_TOKEN)
					
		except FileNotFoundError:
			tokens = error()
			return (True,tokens[0],tokens[1])

