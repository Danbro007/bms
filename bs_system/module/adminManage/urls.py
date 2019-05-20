from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^add/', views.AdminAdd),
    url(r'^list/', views.AdminList),
    url(r'^del/', views.AdminDel),
    url(r'^edit/(?P<id>\d+)/', views.AdminEdit),
    url(r'^data/', views.AdminData),
    url(r'^updatestatus/', views.AccountUpdateStatus),
]

