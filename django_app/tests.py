from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
 
def create_user(self):
    self.client = APIClient()
    self.user = User(first_name='test_user',last_name='test',email=
    'test@gmail.com',username='test',password="abc123")
    self.user.set_password("abc123")
    self.user.save()
    self.token = Token.objects.create(user=self.user)
 
class UserLoginTestCase(APITestCase):
 
    @classmethod
    def setUp(self):
        create_user(self)


    def test_users_view(self):

        #create user
        users_url = reverse('api')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'task': 'test_task', 
            'completed': True, 
            'user': self.user.id
        }
        response = self.client.post(users_url, data=data)
        self.assertEqual(response.status_code,201)

        #List users
        response = self.client.get(users_url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data), 1)

        #get user details
        user_details_url = reverse('api_details', kwargs={'todo_id':self.user.id})
        response =  self.client.get(user_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['task'], 'test_task')

        #update_user_detail
        data = {
            'task': 'test_task1', 
            'completed': True, 
            'user': self.user.id
        }
        response =  self.client.put(user_details_url, data=data)
        self.assertEqual(response.status_code, 200)
        response =  self.client.get(user_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['task'], 'test_task1')


        #delete_user
        response =  self.client.delete(user_details_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(users_url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data), 0)
    
    def tearDown(self):
        # Clean up after each test
        self.user.delete()
