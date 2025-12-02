from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (TeacherProfile, SchoolClass, Subject, Student,
                     InventoryCategory, InventoryItem, BorrowLog, Attendance, Grade)
# Register your models here.

User = get_user_model()
admin.site.register(User)
admin.site.register(TeacherProfile)
admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(InventoryCategory)
admin.site.register(InventoryItem)
admin.site.register(BorrowLog)
admin.site.register(Attendance)
admin.site.register(Grade)