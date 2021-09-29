from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField
from captcha.fields import CaptchaField
from django .core import validators


class NewsForm(forms.Form):
    """create a client class form"""

    title = forms.CharField(max_length=100, label="News title",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="News content", widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "cols": 50,
            "rows": 10})
    )
    is_published = forms.BooleanField(required=False, initial=True,)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(
    ), empty_label="Not chosen", widget=forms.Select(attrs={"class": "form-control"}), label="Category")


class SortingForm(forms.Form):
    """ sort 'new' 'popular' 'most liked'  """

    choice = forms.ChoiceField()


class NewModelForm(forms.ModelForm):
    """ class of creating new post using modelform """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Not chosen"

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 90:
            raise ValidationError("Lenth is more than 90")
        return title

    captcha = CaptchaField(label='Enter the text from the picture',
                           error_messages={'invalid': 'Wrong answer'})
    photo = forms.ImageField(label="Image",
                             validators=[validators.FileExtensionValidator(
                                 allowed_extensions=("gif", "png"))],
                             error_messages={"invalid_extention": """this file format 
                                doesn't support"""})

    class Meta:
        model = Woman
        # rewrite static photo field

        fields = ["title", "content", "photo", "is_published", "cat"]
        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-control'}),
            "views": forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegisterUserForm(UserCreationForm):
    """ Registrating form class """

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = CaptchaField(label='Solve next conundrum',
                           error_messages={'invalid': 'Wrong answer'})

    class Meta:
        model = User

        fields = ( "first_name", "last_name", "username",
                  "email", "password1", "password2",)
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class LoginUserForm(AuthenticationForm):
    """ Login form class """

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User

        fields = ("username", "password",)


class WomanCommentForm(forms.ModelForm):
    """Leaving comment form"""

    username = forms.CharField(max_length=100, label="Username",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             'readonly': True}))
    comment = forms.CharField(label="Comment", widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "cols": 50,
            "rows": 10})
    )

    def clean_username(self):
        user = self.cleaned_data["username"]
        if user != user.title():
            raise ValidationError("Name shold start with an Uppercase letter")
        return user

    class Meta:
        model = WomanComment

        fields = ("username", "comment",)
        readonly_fields = ("username",)


class FeedbackForm(forms.Form):
    """ Send feedback form """

    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email_address = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={
            "class": "form-control",
            "cols": 50,
            "rows": 10}))


class AskPermitionChange(forms.Form): #ask permition when we want to unpublish post 
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)            