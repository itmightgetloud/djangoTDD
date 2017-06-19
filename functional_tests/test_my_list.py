from django.conf import settings
from django.contrib.auth import (
	BACKEND_SESSION_KEY, 
	SESSION_KEY, 
	get_user_model
)
from .base import FunctionalTest
from .test_login import TEST_EMAIL
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
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
		
		#make sure to log out - leftover login from different sessions
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_out(TEST_EMAIL)

		self.create_pre_authenticated_session(TEST_EMAIL)
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_in(TEST_EMAIL)