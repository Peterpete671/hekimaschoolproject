from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import(
    TeacherProfile, SchoolClass, Subject, Student,
    InventoryCategory, InventoryItem, BorrowLog,
    Attendance, Grade
)

User = get_user_model()

#User/Auth
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_teacher', 'is_admin_teacher']
        
class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_teacher']

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user
	
#Core Serializers
class SchoolClassSerializer(serializers.ModelSerializer):
	teacher_name = serializers.ReadOnlyField(source='teacher.username')

	class Meta:
		model = SchoolClass
		fields = ['id', 'name', 'grade_level']


class SubjectSerializer(serializers.ModelSerializer):
	teacher_name = serializers.ReadOnlyField(source='teacher.username')
	class_name = serializers.ReadOnlyField(source='classroom.name')

	class Meta:
		model = Subject
		fields = ['id', 'name', 'teacher', 'teacher_name', 'classroom', 'class_name']

class StudentSerializer(serializers.ModelSerializer):
	class_name = serializers.ReadOnlyField(source='school_class.name')
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = Student
		fields = ['id', 'first_name', 'last_name', 'full_name', 'admission_number', 'school_class', 'school_class', 'class_name', 'date_of_birth']

		def get_full_name(self, obj):
			return f"{obj.first_name} {obj.last_name}"
		
#Inventory serializers
class InventoryCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = InventoryCategory
		fields = ['id', 'name', 'description']

	
class InventoryItemSerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source='category.name')

	class Meta:
		model =  InventoryItem
		fields = ['id', 'name', 'category', 'category_name', 'total_quantity', 'available_quantity', 'description', 'location']

class BorrowLogSerializer(serializers.ModelSerializer):
	item_name = serializers.ReadOnlyField(source='item.name')
	student_name = serializers.ReadOnlyField(source='borrowed_by_student.__str__')
	teacher_name = serializers.ReadOnlyField(source='borrowed_by_teacher.__str__')

	class Meta:
		model = BorrowLog
		fields = ['id','item','item_name','borrowed_by_student','student_name','borrowed_by_teacher','teacher_name','quantity','borrowed_at','returned','returned_at','notes']

#Attendance and Grade
class AttendanceSerializer(serializers.ModelSerializer):
	student_name = serializers.ReadOnlyField(source='student.__str__')
	recorded_by_name = serializers.ReadOnlyField(source='recorded_by.username')

	class Meta:
		model = Attendance
		fields = ['id','student','student_name','date','status','recorded_by','recorded_by_name','note']
		validators = [] #Uniqueness handled by the model unique_together

class GradeSerializer(serializers.ModelSerializer):
	student_name = serializers.ReadOnlyField(source='student.__str__')
	subject_name = serializers.ModelSerializer(source='subject.name')
	recorded_by_name = serializers.ReadOnlyField(source='recorded_by.username')

	class Meta:
		model = Grade
		fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 'score', 'max_score', 'recorded_at', 'recorded_by', 'recorded_by_name']