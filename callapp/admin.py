from django.contrib import admin
from .models import profile, book
from .forms import BookForm

        
@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo','country']


@admin.register(book)
class bookAdmin(admin.ModelAdmin):
    list_display = ['user','name', 'subject', 'message','schedule','identification','date_posted']
    list_filter = ['date_posted']
   
# @admin.register(balance)
# class balanceAdmin(admin.ModelAdmin):
#     list_display = ['user', 'account_balance','date_created']
#     list_filter = ['date_created']