from django.conf import settings
from django.contrib.auth import (
	BACKEND_SESSION_KEY, 
	SESSION_KEY, 
	get_user_model
)
from .base import FunctionalTest
from .test_login import TEST_EMAIL
#from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			#session_key = create_session_on_server(self.staging_server, email)
			print("Uncomment above if running against staging_server")
		else:
			session_key = create_pre_authenticated_session(email)
		"""
		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()
		"""
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(
			dict(
				name=settings.SESSION_COOKIE_NAME,
				value=session_key,
				path='/'		
			)
		)

	def test_logged_in_users_lists_are_save_as_my_list(self):
		
		#user logged in and start by creating two list items
		self.create_pre_authenticated_session(TEST_EMAIL)
		self.browser.get(self.live_server_url)
		self.add_list_item('First item of my own list')
		self.add_list_item('Second item of my own list')
		first_list_url = self.browser.current_url

		#user notices link to the lists owned and decides to click on it
		self.browser.find_element_by_link_text('My lists').click()
		
		#user sees the list called by the first item added
		self.wait_for(lambda: self.browser.find_element_by_link_text('First item of my own list'))
		self.browser.find_element_by_link_text('First item of my own list').click()
		self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

		#user decides to start new list

		self.browser.get(self.live_server_url)
		self.add_list_item('First item on new list')
		second_list_url = self.browser.current_url

		#under my lists newly created list appears

		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(lambda: self.browser.find_element_by_link_text('First item on new list'))
		self.browser.find_element_by_link_text('First item on new list').click()
		self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

		#user can be redirected to add new list from mylists view
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(lambda: self.browser.find_element_by_link_text('Create a new list'))
		self.browser.find_element_by_link_text('Create a new list').click()
		self.wait_for(lambda: self.assertIn(
			'Start',
			self.browser.find_element_by_tag_name('body').text
			)
		)
		
		#user logges out and the My lists option dissapeaars

		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text('My lists'),
            []
        ))

        










