from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter to do item'
		)

		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for rown in rows)
		)
		self.fail('Finish the test')
		#tofinish 
if __name__ == '__main__':
	unittest.main(warnings='ignore')
#print(browser.title)
