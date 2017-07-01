from binarynode import *
import unittest

class BinaryNodeDefaultTestCase(unittest.TestCase):

        
    def setUp(self):
    
        self._ALL = '[(str Alan Iverson, The Answer), (str Alex Rodriguez, A-Rod), (str Daryl Johnson, Moose), (str Dwayne Johnson, The Rock), (str Eldrick Woods, Tiger), (str Gordie Howe, Mr. Hocker), (str Hector Camacho, Macho), (str Ivan Rodrigues, Pudge), (str Jared Lorenzen, The Hefty Lefty), (str Larry Jones, Chipper), (str Maurice Richard, The Rocket), (str OJ Simpson, The Juice), (str Tom Gordon, Flash), (str Walter Payton, Sweetness), (str Wayne Gretsky, The Great One)]'
    
        self._ALL_EXCEPT_WALTER = '[(str Alan Iverson, The Answer), (str Alex Rodriguez, A-Rod), (str Daryl Johnson, Moose), (str Dwayne Johnson, The Rock), (str Eldrick Woods, Tiger), (str Gordie Howe, Mr. Hocker), (str Hector Camacho, Macho), (str Ivan Rodrigues, Pudge), (str Jared Lorenzen, The Hefty Lefty), (str Larry Jones, Chipper), (str Maurice Richard, The Rocket), (str OJ Simpson, The Juice), (str Tom Gordon, Flash), (str Wayne Gretsky, The Great One)]'
    
        self.node = BinaryNode('Dwayne Johnson', 'The Rock')
    	self.node.insert('OJ Simpson', 'The Juice')
    	self.node.insert('Eldrick Woods', 'Tiger')
    	self.node.insert('Tom Gordon', 'Flash')
    	self.node.insert('Jared Lorenzen', 'The Hefty Lefty')
    	self.node.insert('Larry Jones', 'Chipper')
    	self.node.insert('Ivan Rodrigues', 'Pudge')
    	self.node.insert('Hector Camacho', 'Macho') #special char \xc3?
    	self.node.insert('Wayne Gretsky', 'The Great One')
    	self.node.insert('Daryl Johnson', 'Moose')
    	self.node.insert('Gordie Howe', 'Mr. Hocker')
    	self.node.insert('Maurice Richard', 'The Rocket')
    	self.node.insert('Alex Rodriguez', 'A-Rod')
    	self.node.insert('Alan Iverson', 'The Answer')
    	self.node.insert('Walter Payton', 'Sweetness')
    	
    def tearDown(self):
        self.node = None

    def test_key_value_init(self):
        self.assertEqual(self.node._KEY, 'Dwayne Johnson')
        self.assertEqual(self.node._VALUE, 'The Rock')
        
    def test_delete_doesnt_delete_self(self):
	with self.assertRaises(KeyError):
            self.node.delete('Dwayne Johnson')
        self.assertEqual(self.node.inOrder().__repr__(), self._ALL)
        
    def test_delete(self):
        self.assertRaises(KeyError, self.node.delete('Walter Payton'))
        self.assertEqual(self.node.inOrder().__repr__(), self._ALL_EXCEPT_WALTER)
        
    def test_insert(self):
        self.assertEqual(self.node.inOrder().__repr__(), self._ALL)


if __name__ == '__main__':
    unittest.main()
