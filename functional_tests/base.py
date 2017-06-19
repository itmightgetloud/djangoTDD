import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from .server_tools import reset_database


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
	
	def setUp(self):
		#self.display = Display(visible=0, size=(1024,768))
		#self.display.start()
		self.browser = webdriver.Firefox()
		self.staging_server = os.environ.get('STAGING_SERVER')
		if self.staging_server:
			setattr(self, 'live_server_url', 'http://' + self.staging_server)
			reset_database(self.staging_server)
			
	
	def tearDown(self):
		self.browser.quit()
		#self.display.stop()

	def  wait(fn):
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			while True:
				try:
					return fn(*args, **kwargs)
				except (AssertionError, WebDriverException) as error:
					if (time.time() - start_time) > MAX_WAIT:
						raise error
					time.sleep(0.5)
		return modified_fn

	@wait
	def wait_for(self, fn):
		return fn()
	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tbody')
		self.assertIn(row_text, str([row.text for row in rows]))
				
	
	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def  wait_to_be_logged_out(self, email):
		
		self.browser.find_elements_by_tag_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)


