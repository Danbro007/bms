from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^add/', views.CompanyAdd),
    url(r'^list/', views.CompanyList),
    url(r'^del/', views.CompanyDel),
    url(r'^edit/(?P<id>\d+)/', views.CompanyEdit),
    url(r'^data/', views.CompanyData),
]

