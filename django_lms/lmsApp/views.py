import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lmsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import MembersSignUpForm,LoginForm,MemberSignUpForm
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import ChatForm
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from django.shortcuts import render

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

User = get_user_model()

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Library Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")


def Memberregister(request):
    if request.method == 'POST':
        form = MemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_member=True
            user.save()
            messages.success(request, f'Your account has been sent for approval!')
            return redirect('login-page')
        else:
            message = 'form is not valid'
    else:
        form = MemberSignUpForm()
    return render(request,'Members/register.html',{'form':form})




@login_required
def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

# Create your views here.
def login_page(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_admin:
            login(request,user)
            return redirect('home-page')
        elif user is not None and user.is_member: 
            login(request,user)
            return redirect('members-homepage')
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username =form.cleaned_data.get('username')
            password =form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_admin:
                login(request,user)
                return redirect('home-page')
            elif user is not None and user.is_member: 
                login(request,user)
                return redirect('members-homepage')   
            else:   
                msg = 'invalid credentials'
        else:       
            msg = 'error validating form'
    
    return render(request,'logins.html',{'form':form,'msg':msg})


@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag = 0, status = 1).all().count()
    context['members'] = models.Members.objects.filter(delete_flag = 0, status = 1).all().count()
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 2).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['transactions'] = models.Borrow.objects.all().count()

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = models.User.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)
    
    return render(request, 'manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def category(request):
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] = models.Category.objects.filter(delete_flag = 0).all()
    return render(request, 'category.html', context)

@login_required
def save_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            category = models.Category.objects.get(id = post['id'])
            form = forms.SaveCategory(request.POST, instance=category)
        else:
            form = forms.SaveCategory(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Category has been saved successfully.")
            else:
                messages.success(request, "Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
    
    return render(request, 'view_category.html', context)

@login_required
def manage_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
    
    return render(request, 'manage_category.html', context)

@login_required
def delete_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            models.Category.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def sub_category(request):
    context = context_data(request)
    context['page'] = 'sub_category'
    context['page_title'] = "Sub Category List"
    context['sub_category'] = models.SubCategory.objects.filter(delete_flag = 0).all()
    return render(request, 'sub_category.html', context)

@login_required
def save_sub_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            sub_category = models.SubCategory.objects.get(id = post['id'])
            form = forms.SaveSubCategory(request.POST, instance=sub_category)
        else:
            form = forms.SaveSubCategory(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Sub Category has been saved successfully.")
            else:
                messages.success(request, "Sub Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_sub_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_sub_category'
    context['page_title'] = 'View Sub Category'
    if pk is None:
        context['sub_category'] = {}
    else:
        context['sub_category'] = models.SubCategory.objects.get(id=pk)
    
    return render(request, 'view_sub_category.html', context)

@login_required
def manage_sub_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_sub_category'
    context['page_title'] = 'Manage Sub Category'
    if pk is None:
        context['sub_category'] = {}
    else:
        context['sub_category'] = models.SubCategory.objects.get(id=pk)
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_sub_category.html', context)

@login_required
def delete_sub_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Sub Category ID is invalid'
    else:
        try:
            models.SubCategory.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Sub Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Sub Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def books(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = models.Books.objects.filter(delete_flag = 0).all()
    return render(request, 'books.html', context)

@login_required
def save_book(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            book = models.Books.objects.get(id = post['id'])
            form = forms.SaveBook(request.POST, request.FILES,instance=book)
        else:
            form = forms.SaveBook(request.POST,request.FILES) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Book has been saved successfully.")
            else:
                messages.success(request, "Book has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    
    return render(request, 'view_book.html', context)

@login_required
def manage_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_book.html', context)

@login_required
def delete_book(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            models.Books.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def members(request):
    context = context_data(request)
    context['page'] = 'member'
    context['page_title'] = "Member List"
    context['members'] = models.Members.objects.filter(delete_flag = 0).all()
    return render(request, 'members.html', context)

@login_required
def save_member(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            member = models.Members.objects.get(id = post['id'])
            form = forms.SaveMember(request.POST, instance=member)
        else:
            form = forms.SaveMember(request.POST) 

        if form.is_valid():
            # username=form.cleaned_data['username']
            # username.save()
            form.save()
            if post['id'] == '':
                messages.success(request, "Member has been saved successfully.")
            else:
                messages.success(request, "Member has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_member(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_member'
    context['page_title'] = 'View member'
    if pk is None:
        context['member'] = {}
    else:
        context['member'] = models.Members.objects.get(id=pk)
    
    return render(request, 'view_member.html', context)

@login_required
def manage_member(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_member'
    context['page_title'] = 'Manage Member'
    if pk is None:
        context['member'] = {}
    else:
        context['member'] = models.Members.objects.get(id=pk)
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_member.html', context)

@login_required
def delete_member(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Member ID is invalid'
    else:
        try:
            models.Members.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Member has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Member Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def borrows(request):
    context = context_data(request)
    context['page'] = 'borrow'
    context['page_title'] = "Borrowing Transaction List"
    context['borrows'] = models.Borrow.objects.order_by('status').all()
    return render(request, 'borrows.html', context)

@login_required
def save_borrow(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            borrow = models.Borrow.objects.get(id = post['id'])
            form = forms.SaveBorrow(request.POST, instance=borrow)
        else:
            form = forms.SaveBorrow(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Borrowing Transaction has been saved successfully.")
            else:
                messages.success(request, "Borrowing Transaction has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_borrow'
    context['page_title'] = 'View Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = models.Borrow.objects.get(id=pk)
    
    return render(request, 'view_borrow.html', context)

@login_required
def manage_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_borrow'
    context['page_title'] = 'Manage Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = models.Borrow.objects.get(id=pk)
    context['members'] = models.Members.objects.filter(delete_flag = 0, status = 1).all()
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_borrow.html', context)

@login_required
def delete_borrow(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Borrow.objects.filter(pk = pk).delete()
            messages.success(request, "Transaction has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")




class ACreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = models.Chat
    template_name = 'chat_form.html'
    #after posting a chat the user is redirected to his dashboard
    success_url = reverse_lazy('alchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class AListChat(LoginRequiredMixin, ListView):
    model = models.Chat
    template_name = 'chat_list.html'

    def get_queryset(self):
        return models.Chat.objects.filter(posted_at__lt=timezone.now()).order_by('-id')






#members views

def members_home(request):
    NewBooks = models.Books.objects.all()
    return render(request,'Members/index.html',{'NewBooks':NewBooks})
    

def members_register(request):
    if request.method == 'POST':
        form = MembersSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account has been created')
            return redirect('login-page')
        else:
            message = 'form is not valid'
    else:
        form = MembersSignUpForm()
    return render(request,'Members/register.html',{'form':form})  




def members_homepage(request):
    context = context_data(request)
    context['page'] = 'Members home'
    context['page_title'] = 'Members Home'
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['transactions'] = models.Borrow.objects.all().count()

    return render(request, 'Members/home.html', context)




@login_required
def memberborrow(request):
    user = request.user
    books = models.Borrow.objects.filter(member__user=user,borrow="2")
    return render(request, 'Members/viewborrowedbooks.html',{'books':books})




def MemberDetail_save(request):
    user = request.user
    form =forms.MemberDetails()
    mydict={'form':form}
    if request.method == 'POST':
        user = request.POST.get('user')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        form = forms.MemberDetails(request.POST)
        if form.is_valid():
            user=form.cleaned_data['user']
            user.save()

        
        else:
            print("form is invalid")

        report = models.Members.objects.create(

            user = user,
            gender = gender,
            contact = contact,
            address = address,
            )

    return render(request,'Members/members_details.html',context=mydict)

@login_required 
def MemberDetails_save(request):
    if request.method  == 'POST':
        form = forms.MemberDetails(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.user = get_object_or_404(User, user=request.user.id)
            obj.user = User.objects.get(pk=request.user.id)
            obj.save()
            return redirect('members-homepage')
    else:   
        form = forms.MemberDetails()
    return render(request,'Members/members_details.html',{'form':form})


@login_required
def ViewMember(request):
    user = User.objects.get(pk=request.user.id)
    if user == None:
        student = models.Members.objects.filter(user_user=user)
    else:    
        student = models.Members.objects.filter(user=user)
    return render(request,'Members/viewmemberdetails.html',{'user':user,'student':student})




def members_bookpage(request):
    books = models.Books.objects.all()
    return render(request,'Members/bookspage.html',{'books':books})

def Transaction(request):
    user = request.user
    books = models.Borrow.objects.filter(member__user=user,borrow="1")
    return render(request,'Members/transaction.html',{'user':user,'books':books})

def memberfine(request):
    return render(request,'Members/fines.html')


def collections(request):
    result = models.Books.objects.all()
    return render(request, "Members/collections.html", {'BookInformation':result})


def BookInfo(request):    
    result = models.Books.objects.all()
    return render(request, "book_info.html", {'BookInfor':result})




@login_required
def save_transaction(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            borrow = models.Borrow.objects.get(id = post['id'])
            form = forms.SaveBorrow(request.POST, instance=borrow)
        else:
            form = forms.SaveBorrow(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Borrowing Transaction has been saved successfully.")
            else:
                messages.success(request, "Borrowing Transaction has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def manage_transaction(request, pk = None):
    user = request.user
    context = context_data(request)
    context['page'] = 'manage_borrow'
    context['page_title'] = 'Manage Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = models.Borrow.objects.get(id=pk)
    context['members'] = models.Members.objects.filter(user=user)
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'Members/manage_transaction.html', context)

@login_required
def delete_transaction(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Borrow.objects.filter(pk = pk).delete()
            messages.success(request, "Transaction has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")





@login_required(login_url = '/admin_login')
def view_issued_book(request):
    user = request.user
    member = models.Members.objects.all()
    borrow = models.Borrow.objects.filter(borrow="2",status="1")
    li1 = []
    li2 = []

    for i in borrow:
        book = models.Books.objects.filter(isbn=i.book.isbn)
        for book in book:
            t=(request.user.id,request.user.get_full_name, book.isbn, book.title,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*200
        t=(i.issued_date, i.expiry_date, fine)
        li2.append(t)
    return render(request, "fines.html",{'data':zip(li1,li2)})


def issued_books(request):
    user = request.user
    member = models.Members.objects.filter(user_id=request.user.id)
    borrow = models.Borrow.objects.filter(member__user=user,borrow="2",status="1")
    li1 = []
    li2 = []

    for i in borrow:
        book = models.Books.objects.filter(isbn=i.book.isbn)
        for book in book:
            t=(request.user.id,request.user.get_full_name, book.isbn, book.title,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*200
        t=(i.issued_date, i.expiry_date, fine)
        li2.append(t)
    return render(request,'Members/issued_books.html',{'data':zip(li1,li2)})



class UCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = models.Chat
    template_name = 'Members/chats_form.html'
    #after posting a chat the user is redirected to his dashboard
    success_url = reverse_lazy('ulchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UListChat(LoginRequiredMixin, ListView):
    model = models.Chat
    template_name = 'Members/chats_list.html'

    def get_queryset(self):
        return models.Chat.objects.filter(posted_at__lt=timezone.now()).order_by('-id')


