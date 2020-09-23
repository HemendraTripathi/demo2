import sqlite3
from xlsxwriter.workbook import Workbook

def save_to_excel(filename):
	check = True
	try:
		a = open('data','r')
	except FileNotFoundError:
		print("'data' file not found!")
		exit(16)
		
	db_name = a.read()
	a.close()
	workbook = Workbook(filename)
	worksheet = workbook.add_worksheet()
	co = 0
	li = ['data','time','address','user_name','group_name','user_chat_id','order_no','approval']
	conn=sqlite3.connect(db_name)
	c=conn.cursor()
	c.execute("select * from send")
	mysel=c.execute("select * from send")
	for i, row in enumerate(mysel):
		if check == True:
			for col in li:
				worksheet.write(0,co,col)
				co += 1
			check = False
		for j, value in enumerate(row):
			worksheet.write(i+1, j, value)

	workbook.close()
