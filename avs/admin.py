from django.contrib import admin
from .models import UserProfile,Questions,CategoriesQ,Ins,Submission,Testcase
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Questions)
admin.site.register(CategoriesQ)
admin.site.register(Submission)
admin.site.register(Ins)
admin.site.register(Testcase)