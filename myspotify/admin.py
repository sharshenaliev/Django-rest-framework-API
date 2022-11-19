from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Music, Favorites


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'age', 'gender')


class MusicAdmin(admin.ModelAdmin):
    model = Music
    list_display = ('id', 'name', 'author', 'album',  'genre', 'year_published')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('author', 'genre', 'name')


class FavouritesAdmin(admin.ModelAdmin):
    model = Favorites
    list_display = ('id', 'user', 'song')
    list_display_links = ('id', 'user')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Favorites, FavouritesAdmin)
