from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		self.fail('write me!')

