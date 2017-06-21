from django.test import TestCase
from django.contrib.auth import get_user_model
from lists.models import Item, List
from django.core.exceptions import ValidationError

User = get_user_model()

class ItemModelTest(TestCase):
	
	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

class ListModelTest(TestCase):

	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

	def test_create_new_method_creates_list_and_first_item(self):
		List.create_new(first_item_text='new item text')
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'new item text')
		new_list = List.objects.first()
		self.assertEqual(new_item.list, new_list)

	def test_create_new_method_optionally_saves_owner(self):
		user = User.objects.create()
		List.create_new(first_item_text='new item text', owner=user)
		new_list = List.objects.first()
		self.assertEqual(new_list.owner, user)

	def test_lists_can_have_owners(self):
		List(owner=User())

	def test_lists_dont_need_owner(self):
		List().full_clean()

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())

	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()


	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='qwerty')
		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='qwerty')
			item.full_clean()

	def test_can_save_duplicate_items_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='qwerty')
		item = Item(list=list2, text='qwerty')
		item.full_clean()

	def test_list_name_is_same_as_first_item(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='first')
		Item.objects.create(list=list_, text='second')
		self.assertEqual(list_.name, 'first')

	def test_create_returns_new_list_object(self):
		returned = List.create_new(first_item_text='new item text')
		new_list = List.objects.first()
		self.assertEqual(returned, new_list)