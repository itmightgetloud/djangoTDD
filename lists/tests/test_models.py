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

	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

	def test_lists_can_have_owners(self):
		user = User.objects.create(email='a@b.com')
		list_ = List.objects.create(owner=user)
		self.assertIn(list_, user.list_set.all())

	def test_lists_dont_need_owner(self):
		List.objects.create()

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
