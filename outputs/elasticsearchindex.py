import output
import requests
import json
import time

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
                arr['@timestamp'] = str(time.time())
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
