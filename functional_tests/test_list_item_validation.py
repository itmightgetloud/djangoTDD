from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_ITEM_ERROR

class ItemValidationTest(FunctionalTest):

	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')

	def test_cannot_add_empty_list_items(self):
	    # Edith goes to the home page and accidentally tries to submit
	    # an empty list item. She hits Enter on the empty input box
	    self.browser.get(self.live_server_url)
	    self.get_item_input_box().send_keys(Keys.ENTER)

	    # The html5 functionality will intercept the request
	    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))


	    # She tries again with some text for the item, which now works
	    self.get_item_input_box().send_keys('Buy milk')
	    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))


	    self.get_item_input_box().send_keys(Keys.ENTER)
	    self.wait_for_row_in_list_table('1 Buy milk')

	    # Perversely, she now decides to submit a second blank list item
	    self.get_item_input_box().send_keys(Keys.ENTER)

	    # The browser will complain again
	    self.wait_for_row_in_list_table('1 Buy milk')
	    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))		
	    # And she can correct it by filling some text in
	    self.add_list_item('Make tea')
	    
	
	def test_cannot_add_duplicate_items(self):
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys("Duplicate Item")
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1 Duplicate Item")

		self.get_item_input_box().send_keys("Duplicate Item")
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertEqual(self.get_error_element().text, DUPLICATE_ITEM_ERROR))

	def test_error_messages_are_cleared_on_input(self):
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('duplicate item')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 duplicate item')
		self.get_item_input_box().send_keys('duplicate item')
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()
		))


		self.get_item_input_box().send_keys('a')

		self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()
		))