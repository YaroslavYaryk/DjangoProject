from datetime import date
from django.test import SimpleTestCase
from icon.forms import NewModelForm, LoginUserForm, WomanCommentForm, FeedbackForm
from django import forms


class TestForm(SimpleTestCase):

    def setUp(self) -> None:

        self.form = WomanCommentForm(data={
            "username": "Admin",
            "comment": "this is a new comment",

        })

    def test_is_form_post_valid(self):

        self.assertTrue(self.form.is_valid())


    def test_form_with_no_data(self):

        form = WomanCommentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2) 


    def test_is_correct_value_submited(self):

        print(self.form.fields['username'].label, end="\n")  

        self.assertEquals("Username", self.form.fields['username'].label) 


    def test_is_model_form_valid(self):

        feedback_form = FeedbackForm(data={
            'username': "Yaryk31",
            'email_address': 'duhanov1965@gmail.com',
            "message": "here is my message"
        })

        self.assertTrue(feedback_form.is_valid())

    def test_new_post_form_validators(self):

        form =  WomanCommentForm(data={
            "username": "John Dow",
            "comment": 'My peronal comment'
        })  

        self.assertTrue(form.is_valid())

    def test_new_post_form_error_text_validators(self):

        form =  WomanCommentForm(data={
            "username": "John dow",
            "comment": 'My peronal comment'
        })  

        self.assertEquals(form.errors['username'], ["Name shold start with an Uppercase letter"])    