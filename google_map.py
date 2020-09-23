import requests,json
def google_autocomplete(MESSAGE,API_KEY):
	if API_KEY == '':
		print("GOOGLE API KEY NOT FOUND!")
	else:
		url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={MESSAGE}&componenets=country:il&key={API_KEY}'
		try:
			x = requests.get(url)
		except requests.exceptions.ConnectionError:
			print("Check Your Internet Connection !")
			exit(47)
		y = json.loads(x.text)
		predictions = []
		if y['status'] == 'ZERO_RESULTS':
			return [False]
		elif y['status'] == 'OK':
			for prediction in y['predictions']:
				predictions.append(prediction['description'])
		
		return [True,predictions]
