from binarytree import BinaryNode, BinaryTree

# TODO : fix variable names, add exception handling
class AVLnode(BinaryNode):
	def __init__(self,key,value=None):
		"""AVLnode object; inherits from BinaryNode, with added methods
		for rotating left/right and tracking height, balance factor.

		Attributes
		__________

		_HEIGHT : type int
			maximum branch length starting at self. initialized to 1.

		_BALANCE_FACTOR : type int 
			_HEIGHT of right child - _HEIGHT of left child. _HEIGHT = 0 for NoneType"""

		BinaryNode.__init__(self,key,value)
		self._BALANCE_FACTOR = 0
		self._HEIGHT = 1
	
	def adjust_balance_factor(self):
		"""Sets balance factor of self, assuming heights of left child and right child are already correct.
		Applied iteratively moving up tree from root after insertion."""
		left_height = self._LEFT_CHILD._HEIGHT if self._LEFT_CHILD else 0
		right_height = self._RIGHT_CHILD._HEIGHT if self._RIGHT_CHILD else 0
		self._BALANCE_FACTOR = right_height - left_height
		return self._BALANCE_FACTOR

	def adjust_height(self):
		"""Sets self.height assuming heights of left and right children are correct."""
		left_height = self._LEFT_CHILD._HEIGHT if self._LEFT_CHILD else 0
		right_height = self._RIGHT_CHILD._HEIGHT if self._RIGHT_CHILD else 0
		self._HEIGHT = 1 + max(left_height,right_height)
		return self._HEIGHT

	def adjust_size(self):
		"""sets self._SIZE assuming sizes of left and right are correct"""
		left_size = self.left._SIZE if self._LEFT_CHILD else 0
		right_size = self.right._SIZE if self._RIGHT_CHILD else 0
		self._SIZE = 1 + left_size + right_size
		return self._SIZE 
	
	def rotate_left(self):
		"""
		Returns
		_______

		R : type AVLnode
			right child of self, takes place of self in subtree after rotation"""

		if not self._RIGHT_CHILD:
			raise Exception('{} cannot rotate left; has no right node.'.format(self))

		P = self._PARENT
		R = self._RIGHT_CHILD

		self.set_right(R._LEFT_CHILD)
		R.set_left(self)

		# TODO : replace these w .is_right() and .is_left()
		if P and P._KEY < self._KEY:
			P.set_right(R)
		elif P:
			P.set_left(R)
		else:
			R._PARENT = None

		self.adjust_size()
		self.adjust_height()
		self.adjust_balance_factor()

		R.adjust_size()
		R.adjust_height()
		R.adjust_balance_factor()

		if P:
			P.adjust_size()
			P.adjust_height()
			P.adjust_balance_factor()

		return R

	def rotate_right(self):
		if not self._LEFT_CHILD:
			raise Exception('{} cannot rotate right; has no left node.'.format(self))

		P = self._PARENT
		L = self._LEFT_CHILD

		self.set_left(L._RIGHT_CHILD)
		L.set_right(self)

		if P and P._KEY < self._KEY:
			P.set_right(L)
		elif P:
			P.set_left(L)
		else:
			L.parent = None

		self.adjust_size()
		self.adjust_height()
		self.adjust_balance_factor()

		L.adjust_size()
		L.adjust_height()
		L.adjust_balance_factor()

		if P:
			P.adjust_size()
			P.adjust_height()
			P.adjust_balance_factor()

		return L

	def insert(self,key,value=None):
		newNode = AVLnode(key,value)
		stack   = []
		prev 	= None
		current = self

		while current:
			if current.key == key:
				current.value = value
				return
			stack.append(current)
			prev = current
			if current.key < key:
				current = current.right
			else:
				current = current.left

		if prev.key < key:
			prev.set_right(newNode)
		else:
			prev.set_left(newNode)

		# recompute heights and balance factors, rotate subtrees if necessary
		stack.append(newNode)
		newRoot = None
		while stack:
			current = stack.pop()
			current.adjust_size()
			current.adjust_height()
			if current.adjust_balance_factor() > 1:
				
				assert current.balance_factor == 2
				
				if current.right.right and key in current.right.right:
					current = current.rotate_left()
				else:
					current.right = current.right.rotate_right()
					current	= current.rotate_left()
				if not current.parent:
					newRoot = current
			elif current.adjust_balance_factor() < -1:
				
				assert current.balance_factor == -2
				
				if current.left.left and key in current.left.left:
					current	= current.rotate_right()
				else:
					current.left = current.left.rotate_left()
					current	= current.rotate_right()
				if not current.parent:
					newRoot = current
		return newRoot

	def delete(self,key):
		node = self.search(key)
		if node and node is self:
			parent = node.parent
			if not node.left and not node.right:
				if node.is_right():
					parent.right = None
				else:
					parent.left  = None
				del node
				
				current = parent
				while current:
					current.adjust_size()
					current.adjust_height()
					current.adjust_balance_factor()
					current = current.parent
				return
			if node.left and not node.right:
				if node.is_right():
					parent.set_right(node.left)
				else:
					parent.set_left(node.left)

				current = parent 
				while current:
					current.adjust_size()
					current.adjust_height()
					current.adjust_balance_factor()
					current = current.parent
				return

			if node.right and not node.left:
				if node.is_right():
					parent.set_right(node.right)
				else:
					parent.set_left(node.right)

				current = parent
				while current:
					current.adjust_size()
					current.adjust_height()
					current.adjust_balance_factor()
					current = current.parent
				return
			if node.left and node.right:
				minRight = node.min_right()
				rParent  = minRight.Parent
				if minRight is node.right:
					minRight.set_left(node.left)
					if node.is_right():
						parent.set_right(minRight)
					else:
						parent.set_left(minRight)
				else:
					if minRight.right:
						rParent.set_left(minRight.right)
					else:
						rParent.left 	= None
					minRight.set_left(node.left)
					minRight.set_right(node.right)
					if node.is_right():
						parent.set_right(minRight)
					else:
						parent.set_left(minRight)

					current = rParent
					while current:
						current.adjust_size()
						current.adjust_height()
						current.adjust_balance_factor()
						current = current.parent
					return 

class AVLTree(BinaryTree):
	def __init__(self):
		BinaryTree.__init__(self)

	def insert(self,key,value=None):
		if not self.root:
			self.root = AVLnode(key,value)
		else:
			# in case tree has had to rotate from root
			newRoot = self.root.insert(key,value)
			if newRoot:
				self.root = newRoot

	def delete(self,key):
		if self.root and key != self.root._KEY:
			self.root.delete(key)
		elif self.root:
			newRoot = self.root.min_right()
			if (not newRoot) and self.root.left:
				self.root = self.root.left
				self.root.parent = None
			elif newRoot:
				newRoot.parent.left = None
				newRoot.parent = None
			else:
				self.root = None
		else:
			raise KeyError('key {} not in AVLTree'.format(key))
