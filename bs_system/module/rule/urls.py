from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^add/', views.RuleAdd),
    url(r'^list/', views.RuleList),
    url(r'^del/', views.RuleDel),
    url(r'^edit/(?P<id>\d+)/', views.RuleEdit),
    url(r'^data/', views.RuleData),
]

