from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page


"""
class SmokeTest(TestCase):
	def test_bad_maths(self):
		self.assertEqual(1 + 1, 3)
"""
class HomePageTest(TestCase):
	
	"""
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do</title>', html)
		self.assertTrue(html.strip().endswith('</html>'))
	"""
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')		
		
class ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'The first list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Second Item'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_item.text, first_saved_item.text)
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_item.text, second_saved_item.text)
		self.assertEqual(second_saved_item.list, list_)

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

class NewItemTest(TestCase):
	
	def test_can_save_a_POST_request_to_an_existing_list(self):
		
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			f'/lists/{correct_list.id}/add_item', 
			data={'item_text': 'New item on correct_list - existing list'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'New item on correct_list - existing list')
		self.assertEqual(new_item.list, correct_list)
		
	def test_redirects_list_view(self):
		
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post(
			f'/lists/{correct_list.id}/add_item', 
			data={'item_text': 'New item on correct_list'}
		)
		self.assertRedirects(response, f'/lists/{correct_list.id}/')



