from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Review, Title, User


UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    ('Extra Fields', {'fields': ('bio', 'role')}),
)

admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)
