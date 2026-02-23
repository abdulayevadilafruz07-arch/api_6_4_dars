from django.urls import path
from .views import ProductListCreateView

urlpatterns = [
    path('list/', ProductListCreateView.as_view()),

]