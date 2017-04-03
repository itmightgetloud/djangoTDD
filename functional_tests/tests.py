from django.test import LiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.display = Display(visible=0, size=(800,600))
		self.display.start()
		self.browser = webdriver.Firefox()
	def tearDown(self):
		self.browser.quit()
		self.display.stop()
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do', self.browser.title)
		#assert 'To-Do' in browser.title
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter to do item'
		)
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table
		
		self.fail('Finish the test')
		
"""	
	def test_can_add_second_item_and_both_are_visible(self):
		self.browser.get('http://localhost:8000')
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peackock feathers')
		inputbox.send_keys(Keys.ENTER)	 
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('2: Use peackock feathers', [row.text for row in rows])"""

#print(browser.title)
