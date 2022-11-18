from django.urls import path

from .views import *
from .views import AddStockView

urlpatterns = [
    path('addstock/', AddStockView.as_view(), name="addstock"),
    # path('liststock/', ListStock.as_view(), name="liststock")
    path('dashboard/', Turf_Dashboard.as_view(), name="turf_dash"),
    path('schedule', TurfSchedule.as_view(), name="turf_schedule"),
    path('schedule/<slug:id>/', TurfScheduleEdit.as_view(), name="turf_schedule_edit"),
    path('scheduledel/<slug:id>/', TurfScheduleDelete.as_view(), name="turf_schedule_delete"),
    path('manage_user/', ManageUser.as_view(), name="manage_user"),
    path('manage_turf/', ManageTurf.as_view(), name="manage_turf"),
    path('gallery/', Turf_Gallery.as_view(), name="turf_gallery"),
    path('categories/', CategoriesView.as_view(), name="categories"),
    path('categories/<slug:id>/', CategoriesEditView.as_view(), name="categories_edit"),
    path('categoriesdel/<slug:id>/', CategoriesDeleteView.as_view(), name="categories_delete"),
    path('admin/dashboard',AdminDashboardView.as_view(),name="admin_dash"),
    path('deleteturfimag/<int:id>',DeleteGalleryImage.as_view(),name="deleteturfimag"),
    path('galleryupdate',GalleryUpdate.as_view(),name="galleryupdate"),
    path('dashboardimageupdate',DashboardImageUpdate.as_view(),name="dashboardimageupdate"),
    path('dashDataUpdate',dashDataUpdate.as_view(),name="dashDataUpdate"),
    path('DeleteTurfHead',DeleteTurfHead.as_view(),name="DeleteTurfHead"),
    path('TurfPasswordChange',TurfPasswordChange.as_view(),name="TurfPasswordChange"),
    path('TurfCategoryUpdate',TurfCategoryUpdate.as_view(),name="TurfCategoryUpdate")









]