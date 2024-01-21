from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            'Standard info',
            {
                'fields': (
                    'email',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                )
            },
        ),
        ('Extra Fields', {'fields': ('bio', 'role',)}),
    )
