import output
import requests
import json
from datetime import datetime

class ElasticsearchIndex(output.Output):
	requiredData = ["Url","Index"]
	optionalData = []
	def __init__(self,data):
		self.Url=data["Url"]
		self.Index=data["Index"]
	def outputData(self,dataPoints):
		arr = {}
		for i in dataPoints:
			arr[i["name"]] = i["value"]
                arr['messure_date'] = datetime.utcnow().isoformat() + 'Z'
		a = json.dumps(arr)
		try:
			z = requests.post(self.Url,data=a)
                        response = json.loads(z.text)
			if response[u'created'] != True: 
				print "Elasticsearch Error: " + response
				return False
		except Exception:
			return False
		return True
