import os
import poplib
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest
import time
from contextlib import contextmanager

TEST_EMAIL = 'user@example.com'
SUBJECT = 'Your login link for Todo app'

class LoginTest(FunctionalTest):

	@contextmanager
	def pop_inbox(self):
		try:
			inbox = poplib.POP3_SSL(os.environ['TEST_USER_SERVER'])
			inbox.user(os.environ['TEST_USER_LOGIN'])
			inbox.pass_(os.environ['TEST_USER_PASSWORD'])
			yield inbox
		finally:
			inbox.quit()
        
	def wait_for_email(self, test_email, subject):
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(subject, email.subject)
			return email.body
		last_count = 0
		start = time.time()
        
		while time.time() - start < 60:
			with self.pop_inbox() as inbox:
				count, _ = inbox.stat()
				if count != last_count:
					for i in range(count, last_count, -1):
						_, lines, __ = inbox.retr(i)
						lines = [l.decode('utf8', 'ignore') for l in lines]
						if f'Subject: Your login link for Todo app' in lines:
							inbox.dele(i)
							return '\n'.join(lines)
					last_count = count
			time.sleep(5)

	def test_can_get_email_link_to_log_in(self):
		
		if self.staging_server:
			test_email = 'widzew.testuser@gmail.com'
		else:
			test_email = 'user@example.com'

		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
			)
		)

		body = self.wait_for_email(test_email, SUBJECT)

		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.*', body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)

		self.browser.get(url)
		
		#user logged in!
		self.wait_to_be_logged_in(email=test_email)

		#user logs out
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_to_be_logged_out(email=test_email)