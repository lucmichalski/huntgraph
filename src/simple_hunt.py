from graph_utils import *

# Load the provenance Graph
provgraph = nx.read_gpickle("/home/bibek/Chase/huntGraph/data/graph_201")

for node in provgraph.nodes():
	print(node)
	break

for edge in provgraph.edges():
	print(edge)
	break

# to test we will use processes corresponding to execution and lsass_inject event
u = "112b3cf4-df05-40c0-830f-5fd0ac51241e"
v = "38dab005-7bb6-4ba1-8d98-b04b4d17474b"

print(shortest_path(provgraph, u, v))
