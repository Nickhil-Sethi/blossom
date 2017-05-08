_KEY_TYPES = {str : 'str', int : 'int', float : 'float'}

# TODO : key errors, __repr__()

class BinaryNode(object):
	def __init__(self,key,value=None):
		"""BinaryNode object

		Attributes
		__________

		_KEY : type [str, int, float]
			BinaryNode Hash

		_VALUE : arbitrary type 
			value corresponding to key

		_LEFT_CHILD : type binaryNode
			left child of self 

		_RIGHT_CHILD : type binaryNode
			right child of self 

		_SIZE : type int
			size of subtree spanned by self. initialized to 1.

		Methods 
		_______ 

		min_right()
		is_right()
		set_right()
		set_left()
		insert()
		search() 
		inOrder()
		delete()"""

		if type(key) not in _KEY_TYPES:
			raise TypeError('key must be of type str, int, or float.')
		
		# Python doesn't have private variables
		# but this kind of notation is usually used
		# when we don't want a user to be able to access
		# object attributes directly (e.g. change the value of a node's key,
		# which would destroy the order structure of the tree).

		self._KEY = key
		self._VALUE = value
		
		self._LEFT_CHILD = None
		self._RIGHT_CHILD = None
		self._PARENT = None

		self._SIZE = 1

	# TODO : unittest and naming.
	def min_right(self):
		"""Returns minimum element from right subtree, None if right subtree does not exist."""
		prev = None
		current = self._RIGHT_CHILD
		while current:
			prev = current
			current = current._LEFT_CHILD
		return prev

	def is_right(self):
		"""Test for if self is a right child of another node."""

		return (self._PARENT is not None and self._PARENT._KEY < self._KEY)

	def set_left(self,node):
		"""Sets node to self.left, and self to node.parent."""
		
		if node is None:
			if self._LEFT_CHILD is not None:
				self._LEFT_CHILD._PARENT = None
			self._LEFT = None
			return
		self._LEFT_CHILD = node
		node._PARENT = self

	def set_right(self,node):
		"""Sets node to self.right and self to node.parent."""

		if node is None:
			if self._RIGHT_CHILD is not None:
				self._RIGHT_CHILD._PARENT = None
			self._RIGHT_CHILD = None
			return
		self._RIGHT_CHILD = node
		node._PARENT = self

	def insert(self,key,value=None):
		"""Creates binaryNode(key,value) and inserts into subtree of self. 
		If key already exists, sets _VALUE of retrieved key to value

		Parameters
		__________

		key : type [str, int, float] 
			key of binaryNode to be inserted

		value : type arbitrary
			value of binaryNode to be inserted

		Raises
		______ 

		TypeError : key is not in _KEY_TYPES"""

		newNode = BinaryNode(key,value)
		current = self
		
		while current:
			# TODO : is this pythonic ? 
			# Jives with __setitem__ method, which replaces value of OBJ[key]
			# but is a silent fail for some use cases.
			if current._KEY == key:
				current._VALUE = value
				return
			prev = current
			if current._KEY < key:
				current = current._RIGHT_CHILD
			else:
				current = current._LEFT_CHILD
		
		if prev._KEY < key:
			prev.set_right(newNode)
		else:
			prev.set_left(newNode)

		self._SIZE += 1

	def search(self, key):
		"""Binary search for key in subtree of self.

		Parameters
		__________

		key : type [str, int, float]
			key to be searched for in subtree.

		Returns
		_______

		current : type BinaryNode 
			node with _KEY == key

		Raises
		______

		KeyError : while loop exits without key being retrieved."""

		if type(key) not in _KEY_TYPES:
			raise TypeError('key must be of type str, int, or float.')

		prev = None
		current = self
		while current:
			
			if current._KEY == key:
				return current
			prev = current
			if current._KEY < key:
				current = current._RIGHT_CHILD
			else:
				current	= current._LEFT_CHILD

		# raise an error if not present; more pythonic way of exiting.
		raise KeyError('({}, . ) not present in subtree of {}'.format(key,self))


	# TODO : Rename attributes
	def delete(self,key):
		"""Deletes node with key if exists in subtree and is not self.

		Raises
		______

		KeyError : key not in subtree of self"""
		
		node = self.search(key)

		if node != None and node != self:
			self._SIZE -= 1
			parent = node._PARENT
			
			if not (node._LEFT_CHILD or node._RIGHT_CHILD):
				if parent._KEY < node._KEY:
					parent._RIGHT_CHILD = None
				else:
					parent._LEFT_CHILD = None
			
			if node._LEFT_CHILD and not node._RIGHT_CHILD:
				if parent._KEY < node._KEY:
					parent.set_right(node._LEFT_CHILD)
				else:
					parent.set_left(node._LEFT_CHILD)
				node._LEFT_CHILD = None
			
			if node._RIGHT_CHILD and not node._LEFT_CHILD:
				if parent._KEY < node._KEY:
					parent.set_right(node._RIGHT_CHILD)
				else:
					parent.set_left(node._RIGHT_CHILD)
				node._RIGHT_CHILD = None
			
			if node.right and node.left:
				minRight = node.min_right()
				Rparent  = minRight._PARENT
				if minRight is node._RIGHT_CHILD:
					if parent._KEY < node._KEY:
						parent.set_right(minRight)
					else:
						parent.set_left(minRight)
					minRight.set_left(node._LEFT_CHILD)
					node._LEFT_CHILD = None
					node._RIGHT_CHILD = None
				else:
					if minRight._RIGHT_CHILD:
						Rparent.set_left(minRight._RIGHT_CHILD)
						minRight._RIGHT_CHILD = None
					else:
						Rparent._LEFT_CHILD = None
					if parent._KEY < node._KEY:
						parent.set_right(minRight)
					else:
						parent.set_left(minRight)
					minRight.set_left(node._LEFT_CHILD)
					minRight.set_right(node._RIGHT_CHILD)
			del node
			return

	def inOrder(self):
		"""Returns list of elements in subtree recovered by inOrder traversal.

		Returns
		_______

		ret : type list[BinaryNode]
			list of nodes in subtree of self, recovered by inOrder traversal."""
		
		stack = [self]
		# TODO : RENAME THIS
		ret = []
		current = self
		while stack:
			if current._LEFT_CHILD:
				current = current._LEFT_CHILD
				stack.append(current)
			else:
				while stack:
					current = stack.pop()
					ret.append(current)
					if current._RIGHT_CHILD:
						current = current._RIGHT_CHILD
						stack.append(current)
						break
		return ret

	def __repr__(self):
		return "({}, {})".format(self._KEY,self._VALUE)

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
			value of node with node._KEY == key"""

		try:
			node = self.root.search(key)
			return node._VALUE
		except:
			raise KeyError('{} (type {})'.format(key,_KEY_TYPES[type(key)]))
		
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

		KeyError : if key not present """

		if self.root:
			if key == self.root._KEY:
				self.root = None
			else:
				self.delete(key)
		else:
			raise KeyError('{} {}'.format(_KEY_TYPES[type(key)],key))

	def __repr__(self):
		"""returns list of nodes as string, or []"""
		if self.root:
			return str(self.root.inOrder())
		else:
			return '[]'

	def __iter__(self):
		"""iterates nodes of tree by in order traversal"""
		stack = [self.root]
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
	B['6'] = 4
	print B