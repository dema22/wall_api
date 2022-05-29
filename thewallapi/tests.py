from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from thewallapi.models import User, Post

client = APIClient()


def get_client_with_authentication():
    # Login User 2
    client_with_auth = APIClient()
    jwt_fetch_data = {
        'username': 'User2',
        'password': 'mypassword02'
    }
    response = client_with_auth.post('/token/', jwt_fetch_data, format='json')
    access_token = response.data['access']
    client_with_auth.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client_with_auth

class PostsTests(TestCase):
    def setUp(self):
        self.post_author = User.objects.create(username='TestUser',email='test@test.xxx',password='Pass123!!!')
        self.post = Post.objects.create(title='Test Title', content='Test Content', user_id=self.post_author)

    def test_post_is_ok(self):
        post = Post.objects.get(id = self.post.id)
        self.assertEqual(post.title,'Test Title')
        self.assertEqual(post.content,'Test Content')
        self.assertEqual(post.user_id.id,self.post_author.id)

    def tearDown(self):
        self.post_author.delete()
        self.post.delete()

class ApiTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='User1', email='email1@test.com', password='mypassword01')
        self.user2 = User.objects.create_user(username='User2', email='email22@test.com', password='mypassword02')
        self.post = Post.objects.create(title='Post Title', content='Post Content', user_id=self.user1)
        self.post2 = Post.objects.create(title='Post Title2', content='Post Content2', user_id=self.user2)
        self.post3 = Post.objects.create(title='Post Title3', content='Post Content3', user_id=self.user2)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.post.delete()
        self.post2.delete()
        self.post3.delete()

    def test_get_posts_from_all_users(self):
        print('test_get_posts_from_all_users')
        response = client.get('/posts/', format='json')
        json_response = response.json()
        self.assertEqual(len(json_response),3)
        print(response.json())
        self.assertEqual(json_response[0]['content'],self.post3.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print('FINISH test_get_posts_from_all_users')

    def test_successful_registration(self):
        print('test_successful_registration')
        body_data = {
            'username': 'UsernameRegistrationTest',
            'password': 'PasswordRegistrationTest',
            'email': 'registrationtest@test.com',
            'first_name': 'RegistrationNameTest',
            'last_name': 'LastNameRegistrationTest'
        }
        response = client.post('/registration/',body_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'],body_data['username'])
        self.assertEqual(response.json()['email'],body_data['email'])
        print('FINISH test_successful_registration')

    # Testing duplicated registration with username/email already in use by other user (setup: user1).
    def test_duplicated_registration(self):
        print('test_duplicated_registration')
        body_data = {
            'username': 'User1',
            'password': 'password',
            'email': 'email1@test.com'
        }
        response = client.post('/registration/',body_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        print('FINISH test_duplicated_registration')

    def test_failed_login(self):
        print('test_failed_login')
        response = client.post('/token/', {'username': 'User1', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('FINISH test_failed_login')

    def test_create_post_using_another_userid_error(self):
        print('test_create_post_using_another_userid_error')
        client_with_auth = get_client_with_authentication()
        response = client_with_auth.post('/posts/',
                               {'title': 'Creating Post', 'content': 'Trying to post for another account',
                                'user_id': self.user1.id}) #passing other user id account
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('FINISH test_create_post_using_another_userid_error')

    def test_create_post_ok(self):
        print('test_create_post_ok')
        client_with_auth = get_client_with_authentication()
        post_creation_response = client_with_auth.post('/posts/', {'title': 'Creating Post', 'content': 'Post Content!!!', 'user_id': self.user2.id})
        print('En el test, luego de recibir la respuesta del endpoint/post:')
        print(post_creation_response.json())
        print(post_creation_response.status_code)
        self.assertEqual(post_creation_response.status_code, status.HTTP_201_CREATED)
        print('FINISH test_create_post_ok')

    def test_get_profile_information_ok(self):
        print('test_get_profile_information_ok')
        client_with_auth = get_client_with_authentication()
        #
        response = client_with_auth.get('/profile/user/' + str(self.user2.id))
        self.assertEqual(response.json()['id'], self.user2.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('FINISH test_get_profile_information_ok')

    def test_get_all_post_from_logged_user(self):
        print('test_get_all_post_from_logged_user')
        client_with_auth = get_client_with_authentication()
        #
        response = client_with_auth.get('/post/profile/' + str(self.user2.id))
        self.assertEqual(len(response.json()), 2) # asserting that the response is 2 , because user2 has two posts.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('test_get_all_post_from_logged_user')

    def test_get_all_post_from_logged_user_error(self):
        print('test_get_all_post_from_logged_user_error')
        client_with_auth = get_client_with_authentication()
        #
        # Trying to access the post from user1, and we are logged with user2
        response = client_with_auth.get('/post/profile/' + str(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('FINISH test_get_all_post_from_logged_user_error')
