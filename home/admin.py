from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Notes)
admin.site.register(Audio)
admin.site.register(Supporting_Doc)
