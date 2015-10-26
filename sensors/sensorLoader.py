import sys
import ConfigParser
import time
import inspect
import os
import sensor
from sys import exit
from importlib import import_module

class SensorLoader():

    def __init__(self, sensorConfig):
        self.sensorConfig = sensorConfig

    def get_subclasses(self, mod, cls):
        for name, obj in inspect.getmembers(mod):
            if hasattr(obj, "__bases__") and cls in obj.__bases__:
                return obj

    def loadSensors(self):
        sensorPlugins = []
        sensorNames = self.sensorConfig.sections()
        for i in sensorNames:
            try:
                try:
                    filename = self.sensorConfig.get(i,"filename")
                except Exception:
                    print("Error: no filename config option found for sensor plugin " + i)
                    raise
                try:
                    enabled = self.sensorConfig.getboolean(i,"enabled")#
                except Exception:
                    enabled = True

        		#if enabled, load the plugin
                if enabled:
                    try:
                        mod = import_module('sensors.'+filename)
                    except Exception:
                        print("Error: could not import sensor module " + filename)
                        raise

                    try:
                        sensorClass = self.get_subclasses(mod,sensor.Sensor)
                        if sensorClass == None:
                            raise AttributeError
                    except Exception:
                        print("Error: could not find a subclass of sensor.Sensor in module " + filename)
                        raise

                    try:
                        reqd = sensorClass.requiredData
                    except Exception:
                        reqd =  []
                    try:
                        opt = sensorClass.optionalData
                    except Exception:
                        opt = []

                    pluginData = {}

                    class MissingField(Exception): pass

                    for requiredField in reqd:
                        if self.sensorConfig.has_option(i,requiredField):
                            pluginData[requiredField]=self.sensorConfig.get(i,requiredField)
                        else:
                            print "Error: Missing required field '" + requiredField + "' for sensor plugin " + i
                            raise MissingField
                    for optionalField in opt:
                        if self.sensorConfig.has_option(i,optionalField):
                            pluginData[optionalField]=self.sensorConfig.get(i,optionalField)
                    instClass = sensorClass(pluginData)
                    sensorPlugins.append(instClass)
                    print ("Success: Loaded sensor plugin " + i)
            except Exception as e: #add specific exception for missing module
                print("Error: Did not import sensor plugin " + i )
                raise e

        return sensorPlugins
