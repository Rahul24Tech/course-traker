from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from members.models import Contact, Profile
from course_video.models import Course, PlaylistItem
from course_video.forms import AddCourseForm
from members.forms import ContactForm, ProfilePageForm
# Create your tests here.


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('members:signup')
        self.login_url = reverse('members:login')
        self.logout_url = reverse('members:handleLogout')
        self.home_url = reverse('course_video:home')
        self.contact_url = reverse('members:contact')
        self.fav_list = reverse('members:profile_favourite')
        # self.profile_url = reverse('members:show_profile')
        self.register_user = {
            "username": "rahul2",
            "email": "test@gmail.com",
            "password1": "password123@",
            "password2": "password123@"
        }
        self.login_user = {
            "username": "rahul24",
            "password": "password123@"
        }
        self.contact = {
            "name": "Rahul",
            "email": "rahul@gmail.com",
            "phone": "7903381087",
            "content": "I am rahul kumar i am connection techhub admin"
        }
        self.contact_wrong_data = {
            "name": "R",
            "email": "rahul@gmail.com",
            "phone": "79",
            "content": "I rahul"
        }
        self.user = User.objects.create_user(**self.login_user)
        self.profile_info = {
            "user": self.user,
            "bio": "I am new user for testing",
            "profile_pic": "",
            "website_url": "",
            "facebook_url": "",
            "time_preference": "H"
        }
        self.course_data = {
            "link": "https://www.youtube.com/watch?v=FLVB_HruIjk&list=PLx-q4INfd95H5uJKX0edqpbFHVXGrB1Pc&index=7",
            "tags": "django, djangotest"
        }
        self.course = Course.objects.create(author=self.user, title="Django Authentication Tutorial with Unit Testing.",
                                       link="https://www.youtube.com/watch?v=FLVB_HruIjk&list=PLx-q4INfd95H5uJKX0edqpbFHVXGrB1Pc&index=7",
                                       tags="django",
                                       public=True)
        self.playlist = PlaylistItem(
            list_item = "Test driven development",
            time = 619,
            link = "https://www.youtube.com/watch?v=eu0DVe7RkiY&list=PLx-q4INfd95H5uJKX0edqpbFHVXGrB1Pc&index=1&t=15s",
            author=self.user,
            status="Yet to start",
            playlist=self.course
        )

        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.register_user)
        self.assertEqual(response.status_code, 302)


class LoginTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_can_login_user(self):
        self.client.post(self.register_url, self.register_user)
        user = User.objects.filter(email=self.register_user["email"]).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.login_user)
        self.assertEqual(response.status_code, 302)

    def test_can_login_user_with_wrong_username(self):
        login_response = self.client.login(
            username="rahul25", password="password123@")
        if login_response is True:
            response = self.client.get(self.home_url)
            self.assertEqual(response.status_code, 200)

        else:
            print("Username OR Password is incorrect")


class LogoutTest(BaseTest):

    def test_logout(self):
        self.client.login(username='rahul24', password="password123@")

        # Check response code
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)


class ContactTest(BaseTest):

    def test_can_view_contact_page_correctly(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/contact.html')

    def test_can_contact_with_right_input_user(self):
        self.client.login(username='rahul24', password="password123@")
        form = ContactForm(self.contact_wrong_data)
        if form.is_valid():
            if len(form.cleaned_data['name']) < 2 or len(form.cleaned_data['phone']) < 3 or len(form.cleaned_data['email']) < 10 or len(form.cleaned_data['content']) < 4:
                print("Please fill the form correctly")
            else:
                contact = Contact.objects.create(
                    name=self.contact['name'], email=self.contact['email'], phone=self.contact['phone'], content=self.contact['content'])
                contact.save()
                self.assertEqual("Message from " + contact.name + " - " + contact.email,
                                 "Message from " + self.contact['name'] + " - " + self.contact['email'])


class ProfileViewTestCase(BaseTest):

    def test_to_view_profile(self):
        self.user = Profile.objects.get(**self.login_user)
        print(self.user)
        profile_url = reverse('members:show_profile', kwargs={'pk': self.user.id})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)

    def test_to_create_profile(self):
        form = ProfilePageForm(self.profile_info)
        self.assertTrue(form.is_valid())


class FavouriteViewTestCase(BaseTest):

    def test_to_get_all_favourite_data(self):
        course = Course.objects.filter(favourite=self.user)
        response = self.client.get(self.fav_list)
        self.assertIn('course', response.context)
