from provenance import *

def create_graphs():
	provgraph = ProvenanceGraphMaker("/mnt/raid0_ssd_8tb/Bibek/NCR/ecar/evaluation/23Sep19/AIA-201-225/", 201, 225)
	provgraph.getLogFiles()
	provgraph.CreateGraph()
	provgraph.writeGraphs()
#	provgraph.listLogFiles()

if __name__ == "__main__":
	create_graphs()
