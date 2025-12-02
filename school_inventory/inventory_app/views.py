from django import views
from django.shortcuts import render
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import (SchoolClass, Student, Subject, InventoryCategory, InventoryItem, BorrowLog, Attendance, Grade)
from .serializers import (
    SchoolClassSerializer, SubjectSerializer, StudentSerializer, InventoryCategorySerializer, InventoryItemSerializer,
    BorrowLogSerializer, AttendanceSerializer, GradeSerializer, UserSerializer, RegisterSerializer
)
from .permissions import IsAdminTeacher, IsTeacherOrAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from school_inventory.inventory_app import serializers

# Create your views here.

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminTeacher] #Only admin teachers manage users

class RegisterViewSet(views.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'teacher_username']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['classroom', 'teacher']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = InventoryCategorySerializer
    permission_classes = [IsTeacherOrAdmin]

class InventoryCategoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryCategory.objects.all()
    serializer_class = InventoryCategorySerializer
    permission_classes = [IsTeacherOrAdmin]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category_name']
    filterset_fields = ['category', 'location']

    @action(detail=True, methods=['post'], url_path='adjust-stock')
    def adjust_stock(self, request, pk=None):
        """
        Adjust stock(increase or decrease). Body = {"delta": 5}
        Only teacher/admin may adjust.
        """
        item = self.get_object()
        delta =int(request.data.get('delta', 0))
        if delta < 0 and abs(delta) > item.available_quantity:
            return Response({"detail":"Not enough available quantity"}, status=status.HTTP_400_BAD_REQUEST)
        item.total_quantity = max(0, item.total_quantity  + delta)
        item.available_quantity = max(0, item.available_quantity + delta)
        item.save()
        return Response(self.get_serializer(item).data)
    
class BorrowLogViewSet(viewsets.ModelViewSet):
    queryset = BorrowLog.objects.select_related('item', 'borrowed_by_student', 'borrowed_by_teacher').all()
    serializer_class = BorrowLogSerializer
    permission_classes = [IsTeacherOrAdmin]

    def create(self, request, *args, **kwargs):
        """
        Borrow by student or teacher:
        body: {
            "item": 1,
            "borrowed_by_student": 2, # or "borrow_by_teacher": 4
            "quantity": 1
        }
        """

        with transaction.atomic():
            serializer = self.get.serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            item = get_object_or_404(InventoryItem, pk=serializer.validated_data['item'].id if isinstance(serializer.validated_data ['item'], InventoryItem) else serializer.validated_data['item'])
            qty = serializer.validated_data['quantity']
            if item.available.quantity < qty:
                return Response({"detail":"Not enough available quantity"}, status=status.HTTP_400_BAD_REQUEST)
            item.available_quantity -= qty
            item.save()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    @action(detail=True, methods=['post'])
    def return_item(self, request, pk=None):
        borrow = self.get.object()
        if borrow.returned:
            return Response({"detail":"Already returned"}, status=status.HTTP_400_BAD_REQUEST)
        item = borrow.item
        item.available_quantity += borrow.quantity
        item.save()
        borrow.returned = True
        borrow.returned_at = request.data.get('returned_at', None)
        borrow.save()
        return Response(self.get_serializer(borrow).data)
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'date', 'status']

class GradeViewset(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student','subject').all()
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'subject']