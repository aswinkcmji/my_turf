from django.urls import path
from .views import AddStockView
from .views import *


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

]