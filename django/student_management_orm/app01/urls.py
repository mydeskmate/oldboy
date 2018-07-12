from django.conf.urls import url,include
from app01 import views

urlpatterns = [
    url(r'^login.html$',views.login),
    url(r'^classes.html$',views.classes,name="classes"),
    url(r'^add_class/',views.add_class),
    url(r'^del_class/(\d+).html$',views.del_class),
    url(r'^edit_class/(\d+).html$',views.edit_class,name="edit_class"),
]
