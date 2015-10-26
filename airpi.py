#This file takes in inputs from a variety of sensor files, and outputs information to a variety of services
import sys
sys.dont_write_bytecode = True

import RPi.GPIO as GPIO
import ConfigParser
import time
import inspect
import os
from importlib import import_module
from sys import exit
from sensors import sensorLoader
from outputs import output


if not os.path.isfile('sensors.cfg'):
	print "Unable to access config file: sensors.cfg"
	exit(1)

sensorConfig = ConfigParser.SafeConfigParser()
sensorConfig.read('sensors.cfg')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #Use BCM GPIO numbers.

loader = sensorLoader.SensorLoader(sensorConfig)
sensorPlugins = loader.loadSensors()

if not os.path.isfile("outputs.cfg"):
	print "Unable to access config file: outputs.cfg"

outputConfig = ConfigParser.SafeConfigParser()
outputConfig.read("outputs.cfg")

loader = outputLoader.OutputLoader(outputConfig)
outputPlugins = loader.loadOutputs()

if not os.path.isfile("settings.cfg"):
	print "Unable to access config file: settings.cfg"

mainConfig = ConfigParser.SafeConfigParser()
mainConfig.read("settings.cfg")

lastUpdated = 0
delayTime = mainConfig.getfloat("Main","uploadDelay")
redPin = mainConfig.getint("Main","redPin")
greenPin = mainConfig.getint("Main","greenPin")
GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
while True:
	curTime = time.time()
	if (curTime-lastUpdated)>delayTime:
		lastUpdated = curTime
		data = []
		#Collect the data from each sensor
		for i in sensorPlugins:
			dataDict = {}
			val = i.getVal()
			if val==None: #this means it has no data to upload.
				continue
			dataDict["value"] = i.getVal()
			dataDict["unit"] = i.valUnit
			dataDict["symbol"] = i.valSymbol
			dataDict["name"] = i.valName
			dataDict["sensor"] = i.sensorName
			data.append(dataDict)
		working = True
		for i in outputPlugins:
			working = working and i.outputData(data)
		if working:
			print "Uploaded successfully"
			GPIO.output(greenPin,GPIO.HIGH)
		else:
			print "Failed to upload"
			GPIO.output(redPin,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(greenPin,GPIO.LOW)
		GPIO.output(redPin,GPIO.LOW)
