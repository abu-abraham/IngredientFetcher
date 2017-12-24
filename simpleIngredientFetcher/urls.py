from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ingredients/(?P<dish>.*)/$', views.return_ingredients),
    url(r'^fb_bot/*', views.FacebookView.as_view()),
]
