import sys
import ConfigParser
import time
import inspect
import os
import output
from sys import exit
from importlib import import_module

class OutputLoader():

    def __init__(self, outputConfig):
        self.outputConfig = outputConfig

    def get_subclasses(self, mod, cls):
        for name, obj in inspect.getmembers(mod):
            if hasattr(obj, "__bases__") and cls in obj.__bases__:
                return obj

    def loadOutputs(self):
        outputNames = self.outputConfig.sections()
        outputPlugins = []
        for i in outputNames:
        	try:
        		try:
        			filename = self.outputConfig.get(i,"filename")
        		except Exception:
        			print("Error: no filename config option found for output plugin " + i)
        			raise
        		try:
        			enabled = self.outputConfig.getboolean(i,"enabled")
        		except Exception:
        			enabled = True

        		#if enabled, load the plugin
        		if enabled:
        			try:
        				mod = import_module('outputs.'+filename)
        			except Exception:
        				print("Error: could not import output module " + filename)
        				raise

        			try:
        				outputClass = self.get_subclasses(mod,output.Output)
        				if outputClass == None:
        					raise AttributeError
        			except Exception:
        				print("Error: could not find a subclass of output.Output in module " + filename)
        				raise
        			try:
        				reqd = outputClass.requiredData
        			except Exception:
        				reqd =  []
        			try:
        				opt = outputClass.optionalData
        			except Exception:
        				opt = []

        			if self.outputConfig.has_option(i,"async"):
        				async = self.outputConfig.getbool(i,"async")
        			else:
        				async = False

        			pluginData = {}

        			class MissingField(Exception): pass

        			for requiredField in reqd:
        				if self.outputConfig.has_option(i,requiredField):
        					pluginData[requiredField]=self.outputConfig.get(i,requiredField)
        				else:
        					print "Error: Missing required field '" + requiredField + "' for output plugin " + i
        					raise MissingField
        			for optionalField in opt:
        				if self.outputConfig.has_option(i,optionalField):
        					pluginData[optionalField]=self.outputConfig.get(i,optionalField)
        			instClass = outputClass(pluginData)
        			instClass.async = async
        			outputPlugins.append(instClass)
        			print ("Success: Loaded output plugin " + i)
        	except Exception as e: #add specific exception for missing module
        		print("Error: Did not import output plugin " + i )
        		raise e

        return outputPlugins
