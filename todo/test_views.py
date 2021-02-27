from django.test import TestCase
from .models import Item


class TestViews(TestCase):

    # Test HTTP response of the views
    def test_get_todo_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200) #confirms successful HTTP response
        self.assertTemplateUsed(response, 'todo/todo_list.html') #confirms uses correct template

    def test_get_add_item(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_item.html')

    def test_get_edit_item(self):
        item = Item.objects.create(name="Test Todo Item") #need to create a Test item first to edit
        response = self.client.get(f'/edit/{item.id}') #calls items created
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_item.html')

    def test_can_add_item(self):
        response = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/')

    def test_can_delete_item(self):
        item = Item.objects.create(name="Test Todo Item") #create item
        response = self.client.get(f'/delete/{item.id}') #delete item
        self.assertRedirects(response,'/') #check returns to homepage
        existing_items = Item.objects.filter(id=item.id) #to check item deleted, trys to return objects (only 1nr created which was deleted)
        self.assertEqual(len(existing_items), 0) #so length of dict should be 0

    def test_can_toggle_item(self):
        item = Item.objects.create(name="Test Todo Item", done=True) #create item
        response = self.client.get(f'/toggle/{item.id}') #action to toggle item
        self.assertRedirects(response,'/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done) #check item status is now false

    def test_can_edit_item(self):
        item = Item.objects.create(name="Test Todo Item")
        response = self.client.post(f'/edit/{item.id}', {'name': 'Updated Name'}) #post an updated 'name'
        self.assertRedirects(response, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertEqual(updated_item.name, 'Updated Name')
