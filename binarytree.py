from binarynode import BinaryNode

_KEY_TYPES = {str : 'str', int : 'int', float : 'float'}

# TODO : DANGER DELETE FUNCTION HAS LOOP DO NOT USE IT
# TODO : investigate gccollect for BinaryTree; will object be garbage collected?
# TODO : integrate with Python3 ?

class BinaryTree(object):
	def __init__(self):
		"""
		BinaryTree object; wraps all methods of BinaryNode, but acts like Python dict() or set(),
		mapping keys to values, or simply storying values.

		Uses python magic methods e.g. __setitem__, __getitem__.

		Attributes
		__________

		self.root : type BinaryNode"

		
		Methods 
		_______

		__contains__
		__getitem__
		__setitem__
		__delitem__
		__repr__
		__iter__
		__len__"""

		self.root = None

	def __contains__(self,key):
		"""tests for presence/absence of key in self 

		Parameters
		__________

		key : type [ int , str , float ]"""

		try: 
			self.root.search(key)
			return True
		except:
			return False

	def __getitem__(self,key):
		"""
		Parameters
		__________

		key : type [ str , int , float ]
			key of node to search by

		Returns
		_______

		node._VALUE : arbitrary type
			value of node with node._KEY == key
			prints type[key] key that is not present."""

		try:
			node = self.root.search(key)
			return node._VALUE
		except:
			raise KeyError('{} {}'.format(_KEY_TYPES[type(key)],key))
		
	def __setitem__(self,key,value):
		"""inserts BinaryNode(key,value) into self"""
		if not self.root:
			self.root = BinaryNode(key,value)
		else:
			self.root.insert(key,value)

	def __delitem__(self,key):
		"""deletes key from tree

		Raises
		______ 

		KeyError : if key not present"""

		if self.root:
			# TODO : DANGER THIS DOES NOT WORK
			if key == self.root._KEY:
				minRight = self.root.min_right()
				if minRight is None:
					self.root = None
				else:
					if minRight._RIGHT_CHILD is not None and minRight._PARENT is not self.root:
						minRight._PARENT.set_right(minRight._RIGHT_CHILD)
					minRight._PARENT = None
					minRight.set_left(self.root._LEFT_CHILD)
					minRight.set_right(self.root._RIGHT_CHILD)
			else:
				self.root.delete(key)
		else:
			raise KeyError('{} {}'.format(_KEY_TYPES[type(key)],key))

	def __repr__(self):
		"""returns list of nodes as string, or []"""
		if self.root:
			return "BinaryTree({})".format(str(self.root.inOrder()))
		else:
			return 'BinaryTree([])'

	def __iter__(self):
		"""iterates nodes of tree by in order traversal"""
		# would this work?
		# if self.root:
		# 	self.root.__iter__()
		stack = [self.root] if self.root else []
		current = self.root
		while stack:
			if current._LEFT_CHILD:
				current = current._LEFT_CHILD
				stack.append(current)
			else:
				while stack:
					current = stack.pop()
					yield current
					if current._RIGHT_CHILD:
						current = current._RIGHT_CHILD
						stack.append(current)

	def __len__(self):
		"""returns number of nodes in tree"""
		return self.root._SIZE if self.root is not None else 0

def isSorted(arr):
	for i in xrange(len(arr)-1):
		if arr[i] > arr[i+1]:
			return False
	return True

if __name__=='__main__':
	B = BinaryTree()
	B[4] = 'a'
	B[5] = 'b'
	B[3] = 'c'

	del B[4]

	print B