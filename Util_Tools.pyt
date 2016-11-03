# Name:   Util_tools.pyt
# Purpose:   Custom Python Utilities for ArcGIS
# Author:   Andy Bell - ambell@ucdavis.edu
# Created:  11/04/14
#--------------------------------
import os
import arcpy
#import animated_gif


class Toolbox(object):
	def __init__(self):
		self.label = "Util_Tools"
		self.alias = "Util_Tools"

		#list of tool classes associated with the toolbox
		self.tools = [Group2Gif, BatchSymbology]
		

class Group2Gif(object):
	def __init__(self):
		self.label = "Group2Gif"
		self.alias = "Group2GIF"
		self.description = "Iterates over layers in a group and then exports them as sequential images" # TODO: add more info about usage
		self.canRunInBackground = False

	def getParameterInfo(self):

		group = arcpy.Parameter(
			displayName="Group",
		    name = "group",
		    datatype = "GPGroupLayer",
		    parameterType="Required",
		    direction="Input")
		
		output_folder = arcpy.Parameter(
			displayName = "Output Folder Location",
			name = "output_folder",
			datatype = "DEWorkspace",
			parameterType = "Required",
			direction = "Input")

		make_gif = arcpy.Parameter(
			displayName="Make sequential images into GIF?",
		    name = "make_gif",
		    datatype="GPBoolean",
		    parameterType="Optional"
		)

		gif_dur = arcpy.Parameter(
			displayName="GIF loop duration (seconds)",
		    name = "gif_dur",
		    datatype="GPDouble",
		    parameterType="Optional"
		)

		gif_size = arcpy.Parameter(
			displayName="GIF Size",
		    name = "gif_size",
		    datatype="GPDouble",
		    parameterType="Optional"
		)

		parameters = [group, output_folder, make_gif, gif_dur, gif_size]
		return parameters

	def execute(self, parameters, messages):
		group_para = parameters[0].valueAsText
		out_para = parameters[1].valueAsText
		gif_para = parameters[2].valueAsText
		gif_duration = parameters[3].valueAsText
		gif_size = parameters[4].valueAsText

		IMXD = arcpy.mapping.MapDocument("CURRENT") # set current mxd

		# get list of layers in group
		group_layers = []		
		for layer in arcpy.mapping.ListLayers(IMXD):
			if layer.name == group_para:
				arcpy.AddMessage("Inputs: ")
				for subLayer in layer:
					arcpy.AddMessage(subLayer)
					group_layers.append(subLayer)

		# initially turn off layers
		layer_active = {} # dict to store initial visibility of layer.
		for layer in group_layers:
			layer_active[layer] = layer.visible
			layer.visible = False
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()
		
		# iterate over layers in group, turn them on, save as image, then turn off, and repeat
		counter = 0
		
		for layer in group_layers:
			layer.visible = True
			arcpy.RefreshTOC()
			arcpy.RefreshActiveView()
			counter = counter + 1

			# looks for {bind} in any text boxes and will replace it with layer name
			for elm in arcpy.mapping.ListLayoutElements(IMXD, "TEXT_ELEMENT"):
				if elm.text == "{bind}":
					elm.text = layer.name
			
			# output location
			l_name = layer.name
			name = os.path.splitext(l_name)[0] # removes extension
			
			output = os.path.join(out_para, group_para +"_" + name + ".png")
			arcpy.AddMessage(output)

			# save to png
			arcpy.AddMessage(IMXD)
			arcpy.mapping.ExportToPNG(IMXD, output)
			
			arcpy.AddMessage(output)

			# get ready for next layer
			layer.visible = False

			# revert text box back to bind for next layer
			for elm in arcpy.mapping.ListLayoutElements(IMXD, "TEXT_ELEMENT"):
				if elm.text == layer.name:
					elm.text = "{bind}"

		# Turn layers back on
		for layer in group_layers:
			layer.visible = layer_active[layer]

		# refresh view
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()

		# saves sequence as a GIF using images2gif.py and animated_gif.py
		if gif_para == "true":
			print "Saving GIF!!!"
			gif_name = os.path.join(out_para, group_para + ".gif")
			#animated_gif.animated_gif(out_para, gif_name, gif_duration, gif_size)

		# TODO clean up folder, add options for changing direction?


class BatchSymbology(object):
	def __init__(self):
		self.label = "BatchSymbology"
		self.alias = "BatchSymbology"
		self.description = "Applies the same symbology to a list of features"
		self.canRunInBackground = False

	def getParameterInfo(self):

		fcList = arcpy.Parameter(displayName="Input Features", name="fcList", datatype="GPLayer",
		                         parameterType="Required", multiValue=True)

		symbology = arcpy.Parameter(displayName="Symbology Layer", name="symbology", datatype="GPLayer",
		                         parameterType="Required")

		parameters = [fcList, symbology]
		return parameters

	# TODO: add checks to make sure that all feature layers are the same type as the layer symbology

	def execute(self, parameters, messages):
		features_to_symbolize = parameters[0].value.exportToString()
		features_to_symbolize = features_to_symbolize.split(";") # splits multiple features that are separated by ";"
		symbology_layer = parameters[1].valueAsText

		arcpy.AddMessage("Template symbology: %s" % symbology_layer)

		# Process: Apply Symbology From Layer
		for feature in features_to_symbolize:
			arcpy.AddMessage("Symbolizing: %s" % feature)
			arcpy.ApplySymbologyFromLayer_management(feature, symbology_layer)