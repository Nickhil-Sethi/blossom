from collections import OrderedDict

class GenericTreeNode(OrderedDict):
	def __init__(self, *args, **kwargs):
		OrderedDict.__init__(self, *args, **kwargs)

	def insert(self, key, val=None):
		OrderedDict.__setitem__(self, key, val)

	def delete(self, key):
		OrderedDict.popitem(self, key)

class GenericTree(object):
	def __init__(self):
		self.root = GenericTreeNode()

if __name__=='__main__':
	a = GenericTreeNode({'a':1})
	print a
	print a.delete('a')
