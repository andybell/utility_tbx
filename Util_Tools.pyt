# Name:   Util_tools.pyt
# Purpose:   Custom Python Utilities for ArcGIS
# Author:   Andy Bell - ambell@ucdavis.edu
# Created:  11/04/14
#--------------------------------
import os
import arcpy
import animated_gif

class Toolbox(object):
	def __init__(self):
		self.label = "Util_Tools"
		self.alias = "Util_Tools"

		#list of tool classes associated with the toolbox
		self.tools = [group2gif]
		

class group2gif(object):
	def __init__(self):
		self.label = "group2gif"
		self.alias = "Group2GIF"
		self.description = "Iterates over layers in a group and then exports them as sequential images"
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

		parameters = [group, make_gif, output_folder, gif_dur, gif_size]
		return parameters

	def execute(self, parameters, messages):
		group_para = parameters[0].valueAsText
		gif_para = parameters[1].valueAsText
		out_para = parameters[2].valueAsText
		gif_duration = parameters[3].valueAsText
		gif_size = parameters[4].valueAsText

		IMXD = arcpy.mapping.MapDocument("CURRENT") # set current mxd
		
		
		#get list of layers in group
		group_layers = []		
		for layer in arcpy.mapping.ListLayers(IMXD):
			if layer.name == group_para:
				arcpy.AddMessage("Inputs: ")
				for subLayer in layer:
					arcpy.AddMessage(subLayer)
					group_layers.append(subLayer)
		
		
		#initially turn off layers
		layer_active = {} #dict to store inital visibility of layer. TODO: add snippit to turn layers back on.
		for layer in group_layers:
			layer_active[layer] = layer.visible
			layer.visible = False
		arcpy.RefreshTOC()
		arcpy.RefreshActiveView()
		
		#iterate over layers in group, turn them on, save as image, then turn off, and repeat
		counter = 0
		
		for layer in group_layers:
			layer.visible = True
			arcpy.RefreshTOC()
			arcpy.RefreshActiveView()
			counter = counter + 1
			
			#output location
			output = os.path.join(out_para, group_para +"_" + str(counter) + ".png")
			arcpy.AddMessage(output)
			
			
			#save to png
			arcpy.AddMessage(IMXD)
			arcpy.mapping.ExportToPNG(IMXD, output)
			
			arcpy.AddMessage(output)
			layer.visible = False

		if gif_para == "true":
			print "Saving GIF!!!"
			gif_name = os.path.join(out_para, group_para + ".gif")
			animated_gif.animated_gif(out_para, gif_name, gif_duration, gif_size)