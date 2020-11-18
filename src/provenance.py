import os
import sys
import json
import numpy as np
import pandas as pd
import pickle as pkl
import networkx as nx

import re

class ProvenanceGraphMaker():
	def __init__(self, logdir, firsthost, lasthost):
		self.logdir = logdir

		self.graphs = []
		for hostID in range(25):
			G = nx.MultiDiGraph()
			self.graphs.append(G)

		self.hostnames = []
		for hostID in range(firsthost, lasthost+1):
			hostname = "/home/bibek/Chase/huntGraph/data/graph_{}".format(hostID)
			self.hostnames.append(hostname)

		self.logFiles = []

	def getLogFiles(self):
		self.logFiles.clear()
		for dirpath,_,filenames in os.walk(self.logdir):
			for f in filenames:
				if bool(re.search('.json', f)):
					self.logFiles.append(os.path.abspath(os.path.join(dirpath, f)))


	def listLogFiles(self):
		for f in self.logFiles:
			print(f)
		for s in self.hostnames:
			print(s)

	def CreateGraph(self):
		# first pass scan the nodes, and add them
		# Create the process tree
		for fileName in self.logFiles:
			print("Starting {}".format(fileName))
			with open(fileName) as logFile:
				lCount = 0
				for line in logFile:
					line = line.strip()
					try:
						y = json.loads(line)
					except:
						print(line)

					# get the hostname and select correct graph
					idx = int(y["hostname"][10:13]) - 201
					G = self.graphs[idx]

					# now get the subject and objects
					actorId = y["actorID"]
					pid = y["pid"]

					ppid = y["ppid"]
					objectId = y["objectID"]

					objectType = y["object"]
					G.add_node(actorId)

					G.add_node(objectId)
					G.nodes[actorId]["pid"] = pid
					G.nodes[actorId]["ppid"] = ppid
					G.nodes[actorId]["oType"] = "PROCESS"
					G.nodes[actorId]["principal"] = y["principal"]
					G.nodes[actorId]["hostname"] = y["hostname"]
					G.nodes[objectId]["oType"] = objectType

					properties = y["properties"]
					properties["action"] = y["action"]
					properties["timestamp"] = y["timestamp"]
					if y["object"] == "FILE" and y["action"] == "READ":
						G.add_edge(y["objectID"], y["actorID"], attributes = properties)
					elif y["object"] == "MODULE" and y["action"] == "LOAD":
						G.add_edge(y["objectID"], y["actorID"],	attributes = properties)
					elif y["object"] == "FLOW" and y["properties"]["direction"] == "inbound":
						G.add_edge(y["objectID"], y["actorID"], attributes = properties)
					else:
						G.add_edge(y["actorID"], y["objectID"], attributes = properties)

					#processTree.add_edge(ppid, pid)

	def writeGraphs(self):
		for i, G in enumerate(self.graphs):
			nx.write_gpickle(G, self.hostnames[i])



