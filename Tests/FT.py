from pyvirtualdisplay import Display
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.display = Display(visible=0, size=(800,600))
		self.display.start()
		self.browser = webdriver.Firefox()
	def tearDown(self):
		self.browser.quit()
		self.display.stop()
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		#assert 'To-Do' in browser.title
		self.fail("Finish the test")
if __name__ == '__main__':
	unittest.main(warnings='ignore')
#print(browser.title)
