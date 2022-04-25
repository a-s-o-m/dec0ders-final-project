import unittest

#import app from App
from Email import email

class TestRecipes(unittest.TestCase):
    def setUp(self):
        self.email = 'bob@gmail.com'
    def testValues(self):
        # Check when email is not valid
        self.assertRaises(ValueError, 'foobar.com')
    def testUser(self):
        testUser = Email(self.email)
        test_object = set()
    
