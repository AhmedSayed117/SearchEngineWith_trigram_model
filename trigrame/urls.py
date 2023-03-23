from django.contrib import admin
from django.urls import path
from trigramemodel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.build_model, name="build_model"),
    path('search', views.search, name="search"),
    path('suggestion/<str:input>', views.suggestion, name="suggestion"),
]
