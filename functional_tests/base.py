import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
	
	def setUp(self):
		#self.display = Display(visible=0, size=(1024,768))
		#self.display.start()
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server
	
	def tearDown(self):
		self.browser.quit()
		#self.display.stop()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tbody')
				self.assertIn(row_text, str([row.text for row in rows]))
				return
			except (AssertionError, WebDriverException) as error:
				if time.time() - start_time > MAX_WAIT:
					raise error
				time.sleep(0.5)

	def wait_for(self, fn):
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as error:
				if time.time() - start_time > MAX_WAIT:
					raise error
				time.sleep(0.5)
	
	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')