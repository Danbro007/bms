from django.conf.urls import url, include

urlpatterns = [
    url(r'^company/', include("bs_system.module.company.urls")),
    url(r'^position/', include("bs_system.module.position.urls")),
    url(r'^department/', include("bs_system.module.department.urls")),
    url(r'^role/', include("bs_system.module.role.urls")),
    url(r'^rule/', include("bs_system.module.rule.urls")),
    url(r'^admin/', include("bs_system.module.adminManage.urls")),

]
