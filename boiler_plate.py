import requests
from bottle import (run, response, request as bottle_request)

@post('/')
def main():
	data = bottle_requests.json
	get_message
	send_message
	save_to_excel
	return response 
	
if __name__ == '__main__':
	run(host = 'localhost', port = 8080, debug = True)
