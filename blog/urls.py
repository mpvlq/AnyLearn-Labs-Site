from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('api/graph-data/', views.graph_data, name='graph_data'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
