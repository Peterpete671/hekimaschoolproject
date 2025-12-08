from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (TeacherProfile, SchoolClass, Subject, Student,
                     InventoryCategory, InventoryItem, BorrowLog, Attendance, Grade)
# Register your models here.

User = get_user_model()
try:
    admin.site.unregister(User)
except Exception:
    pass
admin.site.register(User, UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(InventoryCategory)
admin.site.register(InventoryItem)
admin.site.register(BorrowLog)
admin.site.register(Attendance)
admin.site.register(Grade)