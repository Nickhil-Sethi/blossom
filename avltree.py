from binarytree import BinaryNode
# TODO : fix variable names, add exception handling
class AVLnode(BinaryNode):
	def __init__(self,key,value=None):
		BinaryNode.__init__(self,key,value)
		self.balance_factor = 0
		self.height = 1
	
	def adjust_balance_factor(self):
		left_height  = self.left.height if self.left else 0
		right_height = self.right.height if self.right else 0
		self.balance_factor = right_height - left_height
		return self.balance_factor

	def adjust_height(self):
		left_height  = self.left.height if self.left else 0
		right_height = self.right.height if self.right else 0
		self.height  = 1 + max(left_height,right_height)
		return self.height

	def adjust_size(self):
		left_size = self.left._SIZE if self.left else 0
		right_size = self.right.size if self.right else 0
		self._SIZE = 1 + left_size + right_size
		return self._SIZE 
	
	def rotate_left(self):
		if not self.right:
			raise Exception('right not present; {} only has {}'.format(self.key,self.inOrder()))

		P = self.parent
		R = self.right

		self.set_right(R.left)
		R.set_left(self)

		if P and P.key < self.key:
			P.set_right(R)
		elif P:
			P.set_left(R)
		else:
			R.parent = None

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
		if not self.left:
			raise Exception('left not present; only has {}'.format(self.inOrder()))
		P 					= self.parent
		L 					= self.left

		self.set_left(L.right)
		L.set_right(self)

		if P and P.key < self.key:
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
			prev 	= current
			if current.key < key:
				current = current.right
			else:
				current = current.left

		if prev.key < key:
			prev.set_right(newNode)
		else:
			prev.set_left(newNode)

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
class AVLTree(object):
	def __init__(self):
		self.root = None

	def insert(self,key,value=None):
		if not self.root:
			self.root     				= AVLnode(key,value)
		else:
			newRoot       				= self.root.insert(key,value)
			if newRoot:
				self.root 				= newRoot

	def size(self):
		return self.root.size if self.root else 0

	def search(self,key):
		if self.root:
			found = self.root.search(key)
			if found:
				return found
		raise KeyError('key {} not in AVLTree'.format(key))

	def delete(self,key):
		if self.root and key != self.root.key:
			self.root.delete(key)
		elif self.root:
			newRoot 	        		= self.root.min_right()
			if (not newRoot) and self.root.left:
				self.root 				= self.root.left
				self.root.parent 		= None
			elif newRoot:
				newRoot.parent.left 	= None
				newRoot.parent      	= None
			else:
				self.root 				= None
		else:
			raise KeyError('key {} not in AVLTree'.format(key))

	def inOrder(self):
		if not self.root:
			return []
		else:
			return self.root.inOrder()

	def __iter__(self):
		"""Iterates through elements via InOrder traversal. Non-recursive implementation."""
		stack = [self]
		current = self
		while stack:
			if current.left:
				current = current.left
				stack.append(current)
			else:
				while stack:
					current = stack.pop()
					yield current
					if current.right:
						current = current.right
						stack.append(current)
						break

		# items = self.inOrder()
		# for item in items:
		# 	yield item
