import output
from datetime import datetime

class Csv(output.Output):
	requiredData = ["File"]
	optionalData = []
	def __init__(self,data):
		self.File = open(data["File"], "a")
	def outputData(self,dataPoints):
                pos = int(self.File.tell())
                date = datetime.utcnow()
                headline = ""
                line = ""
                line = line + date.isoformat() + ";"
                headline = headline + "Date;"
		for i in dataPoints:
                        line = line + '"' + str(i["value"]) + ";"
			headline = headline + i["name"] + "(" + i["symbol"] + ")" + ";"
                if pos == 0:
                        self.File.write(headline + "\n")
                self.File.write(line + "\n")
		return True
