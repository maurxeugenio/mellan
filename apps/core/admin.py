from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Address


class ProfileEdit(admin.StackedInline):
    model = Profile
    can_delete = False
    max_num = 1
    verbose_name = 'Dado do coacho'
    verbose_name_plural = 'Dados do coacho '


class AddressEdit(admin.StackedInline):
    model = Address
    can_delete = False
    max_num = 1
    verbose_name = 'Endereço do usuário'
    verbose_name_plural = 'Endereços do usuário'



class UserAdmin(BaseUserAdmin):
    inlines = (ProfileEdit, AddressEdit)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register((Profile, ))
#admin.site.register(Coach)
