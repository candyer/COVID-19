from flask import Flask, render_template
import requests
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	updated_time, data=get_info()
	data.sort(key=lambda x: x[1], reverse=True)
	total = total_curr_confirmed = total_cured = total_dead = 0

	for name, total_confirmed, curr_confirmed, cured, dead in data:
		total += total_confirmed
		total_curr_confirmed += curr_confirmed
		total_cured += cured
		total_dead += dead
	return render_template(
		'home.html', 
		data = data, 
		total = total, 
		total_curr_confirmed = total_curr_confirmed, 
		total_cured = total_cured, 
		total_dead = total_dead, 
		updated_time = updated_time
	)

def convert_timestamp(timestamp):
	timeStamp = float(timestamp/1000)
	timeArray = time.localtime(timeStamp)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyleTime

def get_info():
	url = 'https://lab.isaaclin.cn/nCoV/api/area'
	res = requests.get(url).json()
	data = []
	updated_time = 0
	for country_data in res['results']:
		if country_data["countryEnglishName"] == 'China':
			if country_data["provinceEnglishName"] == 'China':
				china_total = country_data["confirmedCount"]
				china_curr = country_data["currentConfirmedCount"]
				china_cured = country_data['curedCount']
				china_dead = country_data['deadCount']
				data.append(['China', china_total, china_curr, china_cured, china_dead])
		else:
			if country_data['countryEnglishName']:
				total = country_data['confirmedCount']
				curr = country_data['currentConfirmedCount']	
				cured = country_data['curedCount']		
				dead = country_data['deadCount']
				data.append([country_data['countryEnglishName'], total, curr, cured, dead])
		 
		updated_time = max(updated_time, country_data["updateTime"])
	return convert_timestamp(updated_time), data


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True)

