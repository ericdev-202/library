from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_home',views.home, name="home-page"),
    path('login',views.login_view,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('users',views.users,name='user-page'),
    path('manage_user',views.manage_user,name='manage-user'),
    path('manage_user/<int:pk>',views.manage_user,name='manage-user-pk'),
    path('save_user',views.save_user,name='save-user'),
    path('delete_user/<int:pk>',views.delete_user,name='delete-user'),
    path('category',views.category,name='category-page'),
    path('manage_category',views.manage_category,name='manage-category'),
    path('manage_category/<int:pk>',views.manage_category,name='manage-category-pk'),
    path('view_category/<int:pk>',views.view_category,name='view-category-pk'),
    path('save_category',views.save_category,name='save-category'),
    path('delete_category/<int:pk>',views.delete_category,name='delete-category'),
    path('sub_category',views.sub_category,name='sub_category-page'),
    path('manage_sub_category',views.manage_sub_category,name='manage-sub_category'),
    path('manage_sub_category/<int:pk>',views.manage_sub_category,name='manage-sub_category-pk'),
    path('view_sub_category/<int:pk>',views.view_sub_category,name='view-sub_category-pk'),
    path('save_sub_category',views.save_sub_category,name='save-sub_category'),
    path('delete_sub_category/<int:pk>',views.delete_sub_category,name='delete-sub_category'),
    path('books',views.books,name='book-page'),
    path('manage_book',views.manage_book,name='manage-book'),
    path('manage_book/<int:pk>',views.manage_book,name='manage-book-pk'),
    path('view_book/<int:pk>',views.view_book,name='view-book-pk'),
    path('save_book',views.save_book,name='save-book'),
    path('delete_book/<int:pk>',views.delete_book,name='delete-book'),
    path('members',views.members,name='member-page'),
    path('manage_member',views.manage_member,name='manage-member'),
    path('manage_member/<int:pk>',views.manage_member,name='manage-member-pk'),
    path('view_member/<int:pk>',views.view_member,name='view-member-pk'),
    path('save_member',views.save_member,name='save-member'),
    path('delete_member/<int:pk>',views.delete_member,name='delete-member'),
    path('borrows',views.borrows,name='borrow-page'),
    path('manage_borrow',views.manage_borrow,name='manage-borrow'),
    path('manage_borrow/<int:pk>',views.manage_borrow,name='manage-borrow-pk'),
    path('view_borrow/<int:pk>',views.view_borrow,name='view-borrow-pk'),
    path('save_borrow',views.save_borrow,name='save-borrow'),
    path('delete_borrow/<int:pk>',views.delete_borrow,name='delete-borrow'),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),

    ####chats
    path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
    path('ulchat/', views.UListChat.as_view(), name='ulchat'),
    
    path('acchat/', views.ACreateChat.as_view(), name='acchat'),
    path('alchat/', views.AListChat.as_view(), name='alchat'),


    path('Memberregister/',views.Memberregister, name='member_register'),




    #members
    path('',views.members_home,name="members-home"),
    path('signup/', views.members_register, name='signup'),
    path('members_home',views.members_homepage,name="members-homepage"),
    path('member_borrow',views.memberborrow,name='member-borrow-page'),
    path('member_details',views.MemberDetails_save,name="MemberDetails-save"),
    path('view/',views.ViewMember,name='viewmember'),
    path('members_book_page',views.members_bookpage,name="members-book-page"),
    path('transactions',views.Transaction,name="transaction"),
    path('manage_transaction',views.manage_transaction,name='manage-transaction'),
    path('manage_transaction/<int:pk>',views.manage_transaction,name='manage-transaction-pk'),
    # path('view_transaction/<int:pk>',views.Transaction,name='view-transaction-pk'),
    path('save_transaction',views.save_transaction,name='save-transaction'),
    path('delete_transaction/<int:pk>',views.delete_transaction,name='delete-transaction'),
    path('fines',views.memberfine,name='fines'),
    path('collections',views.collections,name="collection"),
    path('bookinfo',views.BookInfo,name="bookinfo"),
    path("issued_books/", views.issued_books, name="issued_books"),




]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
