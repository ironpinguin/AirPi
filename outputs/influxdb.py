import output
import requests
import json
from datetime import datetime
from influxdb import InfluxDBClient

class InfluxDb(output.Output):
	requiredData = ["Host","Port","Ssl","Database","User","Password","DataHostName"]
	optionalData = []
	def __init__(self,data):
		self.Host=data["Host"]
		self.Port=data["Port"]
		self.Database=data["Database"]
		self.User=data["User"]
		self.Password=data["Password"]
		self.Ssl=data["Ssl"]
		self.dataHostName=data["DataHostName"]
		self.client = InfluxDBClient(self.Host, self.Port, self.User, self.Password, self.Database, self.Ssl)

	def outputData(self,dataPoints):
		timestamp = datetime.utcnow().strftime('%s')
		arr = []
		for i in dataPoints:
			messure_point = {
				"time": timestamp,
				"measurement": "airpi_" + i["name"],
				'fields': {
					'values': i['value']
				},
				'tags': {
					"hostName": self.dataHostName
				}
			}
			arr.append(messure_point)
		try:
			self.client.write_points(arr)
		except Exception:
			return False
		return True
