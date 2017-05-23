from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List

class HomePageTest(TestCase):
	
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')		
		

class ListViewTest(TestCase):
	
	def test_display_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text="item1", list = list_)
		Item.objects.create(text="item2", list = list_)
		
		response = self.client.get(f'/lists/{list_.id}/')
		
		self.assertContains(response, 'item1')
		self.assertContains(response, 'item2')
		
	def test_uses_list_template(self):
		new_list = List.objects.create()
		response = self.client.get(f'/lists/{new_list.id}/')
		self.assertTemplateUsed(response, 'list.html')
	
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			f'/lists/{correct_list.id}/', 
			data={'item_text': 'New item on correct_list - existing list'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'New item on correct_list - existing list')
		self.assertEqual(new_item.list, correct_list)
		
	def test_POST_redirects_to_list_view(self):
		
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post(
			f'/lists/{correct_list.id}/', 
			data={'item_text': 'New item on correct_list'}
		)
		self.assertRedirects(response, f'/lists/{correct_list.id}/')

class NewListTest(TestCase):
	
	def test_can_save_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_validation_errors_are_sent_back_to_home_page_tempate(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't add empty list item")
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)





