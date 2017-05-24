from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
	
	def test_can_start_a_list_for_one_user(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do', self.browser.title)
		#assert 'To-Do' in browser.title
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 Buy peacock feathers')
	
		
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Use peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('2 Use peacock feathers')
		self.wait_for_row_in_list_table('1 Buy peacock feathers')
	
		
	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 Buy peacock feathers')
		first_user_list_url = self.browser.current_url
		self.assertRegex(first_user_list_url, '/lists/.+')
		
		#exit browser and open a new window for new user
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		self.browser.get(self.live_server_url)
		page_body = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_body)
		
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy Milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 Buy Milk')
		second_user_list_url = self.browser.current_url
		self.assertRegex(second_user_list_url, '/lists/.+')
		self.assertNotEqual(first_user_list_url, second_user_list_url)