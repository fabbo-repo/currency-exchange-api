from django.contrib.auth.models import Group, User
from django.contrib import admin

# Remove Groups from admin
admin.site.unregister(Group)
# Remove Users from admin
admin.site.unregister(User)
