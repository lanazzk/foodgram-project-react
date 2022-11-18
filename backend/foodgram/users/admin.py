from django.contrib import admin

from .models import CustomUser

admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = '__all__'
    search_fields = ('username', 'email', )
    list_filter = ('username', 'email', )
