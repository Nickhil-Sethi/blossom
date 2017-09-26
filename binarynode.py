# TODO : UnitTest inOrder(); most fundamental function to test others
# TODO : rewrite inOrder() more elegantly? 

_KEY_TYPES = {str : 'str', int : 'int', float : 'float'}

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

	def is_left(self):
		"""Test for if self is a left child of another node."""
		return (self._PARENT is not None and self._PARENT._KEY > self._KEY)

	def set_left(self,node):
		"""Sets node to self.left, and self to node.parent."""
		if node is None:
			if self._LEFT_CHILD is not None:
				self._LEFT_CHILD._PARENT = None
			self._LEFT_CHILD = None
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
		If key already exists, overrides node._VALUE of retrieved node to value

		Parameters
		__________

		key : type [str, int, float] 
			key of binaryNode to be inserted

		value : type arbitrary
			value of binaryNode to be inserted

		Raises
		______ 

		TypeError : key is not in _KEY_TYPES"""

		if not isinstance(key, BinaryNode):
			newNode = BinaryNode(key,value)
		else:
			newNode = key

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

		current = self
		while current:
			if current._KEY == key:
				return current
			if current._KEY < key:
				current = current._RIGHT_CHILD
			else:
				current	= current._LEFT_CHILD
		
		# raise KeyError if not found
		if type(key) is str:
			raise KeyError("'{}' not present in subtree of {}".format(key,self))
		raise KeyError("{} not present in subtree of {}".format(key,self))


	# TODO : Rename attributes
	def delete(self,key):
		# TODO : THIS DOES NOT WORK
		"""Deletes node with key if exists in subtree and is not self.

		Raises
		______

		KeyError : key not in subtree of self"""
		
		node = self.search(key)

		# a node cannot delete itself
		# root deletion function is handled as a special case
		if node is not self:
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
			
			if node._RIGHT_CHILD and node._LEFT_CHILD:
				minRight = node.min_right()
				Rparent  = minRight._PARENT
				if minRight is node._RIGHT_CHILD:
					# set parent.right is minRight
					if parent._KEY < node._KEY:
						parent.set_right(minRight)
					else:
						parent.set_left(minRight)

					minRight.set_left(node._LEFT_CHILD)
					node._LEFT_CHILD = None
					node._RIGHT_CHILD = None
					node._PARENT = None
				else:
					if minRight._RIGHT_CHILD:
						Rparent.set_left(minRight._RIGHT_CHILD)
						minRight._RIGHT_CHILD = None
						minRight._PARENT = None
					else:
						Rparent._LEFT_CHILD = None
						minRight._PARENT = None
					
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
		
		# TODO : RENAME THIS
		ret = []
		stack = [self]
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

	def __contains__(self,key):
		"""Test for presence/absence of node w ._KEY == key in subtree of self"""
		try:
			self.search(key)
			return True
		except:
			return False

	def __repr__(self):
		if type(self._KEY) is str:
			return "('{}', {})".format(self._KEY, self._VALUE)
		return "({}, {})".format(self._KEY,self._VALUE)

if __name__=='__main__':
	import numpy as np
	B = BinaryNode(np.random.randint(1000))

	for j in xrange(100):
		for i in xrange(10000):
			B.insert(np.random.randint(1000))

		l = B.inOrder()

		for node in l:
			# print "Deleteing {}".format(node)
			B.delete(node._KEY) 

