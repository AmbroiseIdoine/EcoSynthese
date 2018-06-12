from django.urls import path
from . import views

app_name = 'ecosyn'
urlpatterns = [
    path('', views.home, name='home'),
    path('apropos', views.apropos, name='apropos'),
    path('sources', views.sources, name='sources'),
    path('contact/', views.ContactView.as_view(), name= 'contact'),
    path('reports/', views.ReportView.as_view(), name= 'reports'),
    path('topics/', views.TopicView.as_view(), name='topics'),
    path('<int:pk>/reports/', views.ReportDetailView.as_view() , name= 'report_details'),
    path('<int:pk>/topics/', views.TopicDetailView.as_view() , name='topic_details'),
    path('page/<str:page_name>/', views.page_view , name='page'),
    ]
