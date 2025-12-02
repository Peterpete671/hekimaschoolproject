from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	is_teacher = models.BooleanField(default=False)
	is_admin_teacher = models.BooleanField(default=False) #The School Admin

	def __str__(self):
		return self.get_full_name() or self.username

class TeacherProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
	phone = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return str(self.user)

class SchoolClass(models.Model):
	name = models.CharField(max_length=50) #Grade 8 Green
	teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='classes')

	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=100)
	teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	classroom = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')

	def __str__(self):
		return self.name

class Student(models.Model):
	first_name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	admission_number = models.CharField(max_length=50, unique=True)
	school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, related_name='students')
	date_of_birth = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.admission_number})"


#inventory models
class InventoryCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class InventoryItem(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(InventoryCategory, on_delete=models.SET_NULL, null=True, related_name='items')
	total_quantity = models.PositiveIntegerField(default=0)
	available_quantity = models.PositiveIntegerField(default=0)
	description = models.TextField(blank=True)
	location = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.name

class BorrowLog(models.Model):
	item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='borrow_logs')
	borrowed_by_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
	borrowed_by_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	borrowed_at = models.DateTimeField(auto_now_add=True)
	returned = models.BooleanField(default=False)
	returned_at = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		who = self.borrowed_by_teacher or self.borrowed_by_student
		return f"{self.borrowed_by_teacher} x{self.quantity} by {who}"

#Attendance
class Attendance(models.Model):
	ATTENDANCE_STATUS = (
		('present', 'Present'),
		('absent', 'Absent'),
		('late', 'Late'),
		('excused', 'Excused'),
	)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
	date = models.DateField()
	status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)
	recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	note = models.TextField(blank=True)

	class Meta:
		unique_together = ('student','date')

	def __str__(self):
		return f"{self.student} - {self.date} - {self.status}"

class Grade(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
	score = models.DecimalField(max_digits=5, decimal_places=2)
	max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
	recorded_at = models.DateTimeField(auto_now_add=True)
	recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f"{self.student} - {self.subject} : {self.score}/{self.max_score}"
