# encoding=utf8  
import sys  
import requests
import re
import csv
import json 
import os.path

def build_dictionary():
        response = requests.post("https://www.aliaspa.it/puliziastrade/index.php/main/get_indirizzi", data={'comune': 'FIRENZE'})
        print(response.status_code, response.reason)
        js = json.loads(response.text.replace("&#039;", "'"))
        with open("roads.csv", "w", newline='') as ffile:
            file = csv.writer(ffile)
            file.writerow(["id_strada", "nome"])
            for road in js:
                file.writerow([road["id_strada"], road["nome"]])
        mydict = {}
        # reverse dictionary
        with open('roads.csv', "r") as infile:
            reader = csv.reader(infile)
            mydict = {rows[1]:rows[0] for rows in reader}
        #for id_strada in mydict.values():
        	#get_road_stretch(id_strada)
        return mydict

def get_schedule(id_strada):
	TAG_RE = re.compile(r'<[^>]+>')
	if os.path.exists(id_strada+".json"):
		pass
		# send tratto
	r = requests.post("https://www.aliaspa.it/puliziastrade/index.php/pulizie/calcola_data", data={'id_strada': id_strada, 'trattostrada': ''})
	print(r.status_code, r.reason, r.encoding)
	text = TAG_RE.sub('', r.text).replace("\u00e8", "è").replace(r'\t', '\n').replace('&ordm', '°').replace('&times;\n', '').replace('\/', '/').replace('8O', '8 --- O').replace("&egrave;", "è")
	return text

def get_road_stretch(id_strada):
	response = requests.post("https://www.aliaspa.it/puliziastrade/index.php/main/get_tratti", data={'id_strada': id_strada})
	if response.text != 'null':
		print(response.text == 'null') 
		data = json.loads(response.text)
		with open(id_strada+".json", "w") as file:
			json.dump(data, file)
		#stretches = []
		#for dat in data:
		#	stretches.append(list(data.values()))