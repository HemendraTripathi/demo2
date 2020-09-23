#Shree Ganesh#
from bottle import (run, post, response, request as bottle_request)
import os,sqlite3,requests,json,sys,datetime
from xlsxwriter.workbook import Workbook
from ver import verify_input
from time import sleep
from get_user import get_user
from get_message import get_message
from send_message import send_message
from save_to_excel import save_to_excel



flag, TOKEN, API_TOKEN = verify_input(sys.argv)
if not flag:
	sys.exit(3)
current_month_text = datetime.datetime.now().strftime('%B')
current_year_text = datetime.datetime.now().strftime('%Y')
sheet_name = current_month_text +"_"+current_year_text+".xlsx"
url = f'https://api.telegram.org/bot{TOKEN}/'
webhook_url = input("Enter Webhook URL : ")

try:
	web = requests.get(url+'deletewebhook')
	print("\nPrevious WebHook Deleted.")
except requests.exceptions.ConnectionError:
	print("Please Check Your Internet Connection! WEBHOOK")
	exit(6)

try:
	web = requests.get(url+'setWebHook?url='+webhook_url)
	print("\nWebhook Setted....\n")
except requests.exceptions.ConnectionError:
	print("Please Check Your Internet Connection! WEBHOOK2")
	exit(5)

cwd = os.getcwd()
path = os.path.join(cwd,'delivery_data')
print(path)
try:
	os.mkdir(path)
	print(path)
except FileExistsError:
	pass
sheet_name = os.path.join(path,sheet_name)
print(sheet_name)
@post('/')
def main():
	data = bottle_request.json
	get_user(TOKEN)
	get_message(TOKEN,API_TOKEN,data)
	send_message(TOKEN)
	save_to_excel(sheet_name)
	if sys.platform == 'win32':
		os.system('cls')
	elif sys.platform == 'linux':
		os.system('clear')
	print("""
	
Refreshing ............

      )  (
     (   ) )
      ) ( (
    _______)_
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'

	""")
	return response

if __name__ == '__main__':
	run(host = 'localhost', port = 8080, debug = True)
	
	
	
	
