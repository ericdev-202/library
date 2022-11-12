from datetime import datetime
from random import random
from secrets import choice
from sys import prefix
from unicodedata import category
from django import forms
from numpy import require
from lmsApp import models

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()



class SaveUser(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1','is_member', 'password2',)

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateUser(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class SaveCategory(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Category
        fields = ('name', 'description', 'status', )

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                category = models.Category.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                category = models.Category.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Category Name already exists.")

class SaveSubCategory(forms.ModelForm):
    category = forms.CharField(max_length=250)
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.SubCategory
        fields = ('category', 'name', 'description', 'status', )

    def clean_category(self):
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        try:
            category = models.Category.objects.get(id = cid)
            return category
        except:
            raise forms.ValidationError("Invalid Category.")

    def clean_name(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            category = models.Category.objects.get(id = cid)
            if id > 0:
                sub_category = models.SubCategory.objects.exclude(id = id).get(name = name, delete_flag = 0, category = category)
            else:
                sub_category = models.SubCategory.objects.get(name = name, delete_flag = 0, category = category)
        except:
            return name
        raise forms.ValidationError("Sub-Category Name already exists on the selected Category.")
     
class SaveBook(forms.ModelForm):
    sub_category = forms.CharField(max_length=250)
    isbn = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    description = forms.Textarea()
    images = forms.FileField()
    author = forms.Textarea()
    publisher = forms.Textarea()
    date_published = forms.DateField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Books
        fields = ('isbn', 'sub_category', 'images','title', 'description', 'author', 'publisher', 'date_published', 'status', )

    def clean_sub_category(self):
        scid = int(self.data['sub_category']) if (self.data['sub_category']).isnumeric() else 0
        try:
            sub_category = models.SubCategory.objects.get(id = scid)
            return sub_category
        except:
            raise forms.ValidationError("Invalid Sub Category.")

    def clean_isbn(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        isbn = self.cleaned_data['isbn']
        try:
            if id > 0:
                book = models.Books.objects.exclude(id = id).get(isbn = isbn, delete_flag = 0)
            else:
                book = models.Books.objects.get(isbn = isbn, delete_flag = 0)
        except:
            return isbn
        raise forms.ValidationError("ISBN already exists on the Database.")
  
class SaveMember(forms.ModelForm):
    code = forms.CharField(max_length=250)
    # user = forms.CharField(max_length=250)
    user = forms.CharField(max_length=250)
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    department = forms.CharField(max_length=250)
    address = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Members
        fields = ('code','user','gender', 'contact', 'email', 'address', 'department',  'status')

    def clean_user(self):
        user = int(self.data['user']) if (self.data['user']).isnumeric() else 0
        try:
            user = models.User.objects.get(id = user)
            return user
        except:
            raise forms.ValidationError("Invalid user.") 

    def clean_code(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            if id > 0:
                book = models.Books.objects.exclude(id = id).get(code = code, delete_flag = 0)
            else:
                book = models.Books.objects.get(code = code, delete_flag = 0)
        except:
            return code
        raise forms.ValidationError("Members Id already exists on the Database.")
    
class SaveBorrow(forms.ModelForm):
    member = forms.CharField(max_length=250)
    book = forms.CharField(max_length=250)
    issued_date = forms.DateField()
    borrow = forms.CharField(max_length=2)
    expiry_date = forms.DateField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Borrow
        fields = ('member', 'book', 'expiry_date','borrow', 'status', )

    def clean_member(self):
        member = int(self.data['member']) if (self.data['member']).isnumeric() else 0
        try:
            member = models.Members.objects.get(id = member)
            return member
        except:
            raise forms.ValidationError("Invalid member.")
            
    def clean_book(self):
        book = int(self.data['book']) if (self.data['book']).isnumeric() else 0
        try:
            book = models.Books.objects.get(id = book)
            return book
        except:
            raise forms.ValidationError("Invalid Book.")


class MembersSignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
            "class":"form-control"
            }
            )
        )
    email = forms.CharField(
        widget = forms.TextInput(
            attrs={
            "class":"form-control"
            })
        )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
            "class":"form-control"
            }
            ))
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
            "class":"form-control"
            }))
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
            "class":"form-control"
            }
            )
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "class":"form-control"
            }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class MemberDetails(forms.ModelForm):
    
    class Meta:
        model = models.Members
        address = forms.ChoiceField(
            widget = forms.TextInput(
                attrs={
                "class":"form-control"
                 }))
        contact = forms.CharField(
            widget= forms.TextInput(
                attrs={
                "class":"form-control-label"
                }))
        gender = forms.CharField(
            widget = forms.TextInput(
                attrs={
                "class":"form-control"
                }))


        fields =('gender', 'contact', 'address')
        def clean(self):
            cleaned_data = super().clean()
            user = cleaned_data.get('user')
            created = datetime.now().date()
            if Member.objects.filter(user=user, created=created).exists():
                raise forms.ValidationError("User already filles the form")

class MemberDetail(forms.ModelForm):
    # code = forms.CharField(max_length=250)
    # user = forms.CharField(max_length=250)
    user =forms.ModelChoiceField(queryset=models.User.objects.all(),empty_label=" Details",to_field_name='id')
    # user = forms.CharField(max_length=250)
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    # email = forms.CharField(max_length=250)
    # department = forms.CharField(max_length=250)
    address = forms.Textarea()
    # status = forms.CharField(max_length=2)

    class Meta:
        model = models.Members
        fields = ('gender', 'contact', 'address')

    def clean_user(self):
        user = int(self.data['user']) if (self.data['user']).isnumeric() else 0
        try:
            user = models.User.objects.get(id = user)
            return user
        except:
            raise forms.ValidationError("Invalid user.") 

    def clean_code(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            if id > 0:
                book = models.Books.objects.exclude(id = id).get(code = code, delete_flag = 0)
            else:
                book = models.Books.objects.get(code = code, delete_flag = 0)
        except:
            return code
        raise forms.ValidationError("Members Id already exists on the Database.")

        fields =('student_name','university_name' ,'coursename','regno','year_of_study','school')
        def clean(self):
            cleaned_data = super().clean()
            user = cleaned_data.get('user')
            created = datetime.now().date()
            if Student.objects.filter(user=user, created=created).exists():
                raise forms.ValidationError("User already filles the form")



class ChatForm(forms.ModelForm):
    message = forms.Textarea()
    class Meta:
        model = models.Chat
        fields = ('message', )



class MemberSignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
            "class":"form-control"
            }
            )
        )
    email = forms.CharField(
        widget = forms.TextInput(
            attrs={
            "class":"form-control"
            })
        )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
            "class":"form-control"
            }
            ))
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs={
            "class":"form-control"
            }))
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
            "class":"form-control"
            }
            )
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "class":"form-control"
            }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','is_member','password1', 'password2')


