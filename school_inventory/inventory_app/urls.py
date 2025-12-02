from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RegisterViewSet,
    SchoolClassViewSet, SubjectViewSet, StudentViewSet,
    InventoryCategoryViewSet, InventoryItemViewSet, BorrowLogViewSet,
    AttendanceViewSet, GradeViewset
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('register', RegisterViewSet, basename='register')
router.register('classes', SchoolClassViewSet)
router.register('subjects', SubjectViewSet)
router.register('students', StudentViewSet)
router.register('inventory/categories', InventoryCategoryViewSet, basename='Inventory-categories')
router.register('inventory/items', InventoryItemViewSet, basename='inventory_categories')
router.register('inventory/borrow', BorrowLogViewSet, basename='borrow')
router.register('attendance', AttendanceViewSet)
router.register('grades', GradeViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]