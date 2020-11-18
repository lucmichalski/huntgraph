import os
import sys
import re
import json

import networkx as nx
import pandas as pd
import pickle as pkl
import numpy as np

def shortest_path(G, u, v):
	try:
		return nx.shortest_path(G, u, v);
	except:
		return "INFINITY"

