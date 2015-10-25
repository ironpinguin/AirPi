import output
import requests
import time
from requests.auth import HTTPBasicAuth

class InfluxDb(output.Output):
	requiredData = ["Host","Port","Ssl","Database","User","Password","DataHostName"]
	optionalData = []
	def __init__(self,data):
		self.Url = "http://"
		if (data["Ssl"]):
			self.Url = "https://"
		self.Url += data["Host"]
		self.Url += ":" + data["Port"]
		self.Database=data["Database"]
		self.User=data["User"]
		self.Password=data["Password"]
		self.Ssl=data["Ssl"]
		self.dataHostName=data["DataHostName"]

	def outputData(self,dataPoints):
		nanotimestamp = ("%.9f" % time.time()).replace('.','')
		messure_points = []
		for i in dataPoints:
			messure_point = "airpi_" + i['name']
			messure_point += ",host=" + self.dataHostName
			messure_point += ",symbol=" + i['symbol']
			messure_point += " value=" + str(i['value'])
			messure_point += " " + nanotimestamp
			messure_points.append(messure_point)
		postBody = "\n".join(messure_points)
		try:
			z = requests.post(
				self.Url + "/write?db=" + self.Database,
				verify=False,
				auth=HTTPBasicAuth(self.User, self.Password),
				data=postBody
			)
			if z.status_code != 204:
				print "InfluxDb Error: " + z.text
				return False
		except Exception:
			return False
		return True
