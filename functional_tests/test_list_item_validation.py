from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id("id_new_item")
		inputbox.send_keys(Keys.ENTER)

		self.wait_for(
			lambda:self.assertEqual(
				self.browser.find_element_by_css_selector('.has-error').text,
				"You can't add empty list item"
			)
		)

		inputbox.send_keys('This time not empty')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 This time not empty')

		inputbox.send_keys(Keys.ENTER)
		self.wait_for(
			lambda:self.assertEqual(
				self.browser.find_element_by_css_selector('.has-error').text,
				"You can't add empty list item"
			)
		)

		inputbox.send_keys("Another not empty entry")
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 This time not empty')
		self.wait_for_row_in_list_table('2 Another not empty entry')


