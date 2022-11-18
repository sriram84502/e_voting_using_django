from django.contrib import admin
from .models import CustomUser,participants,Profile,Voters,Votingrelease,Resultrelease
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    list_display = ('username', 'name', 'phone','district','is_active','mandal')
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Personal info', 
            {
                'fields': (
                    'name',
                    'phone',
                    'is_phone_verified',
                    'district',
                    'mandal',
                )
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','name', 'is_phone_verified' , 'is_active' , 'password', 'password1','phone' , 'district' , 'mandal')}
         ),
    )
   
admin.site.register(CustomUser, CustomUserAdmin)

class Customvoters(admin.ModelAdmin):
    list_display = ('user',)
admin.site.register(Voters,Customvoters)

class Customdvotedisplay(admin.ModelAdmin):
    list_display = ('time','voting',)
admin.site.register(Votingrelease,Customdvotedisplay)

class Customdresultdisplay(admin.ModelAdmin):
    list_display = ('time','result',)
admin.site.register(Resultrelease,Customdresultdisplay)


class Customprofile(admin.ModelAdmin):
    list_display = ('user','phone1','aadhar1',)
admin.site.register(Profile,Customprofile)


class CustomParticipant(admin.ModelAdmin):
    list_display = ('id','name','district','mandal','votes')

admin.site.register(participants,CustomParticipant)