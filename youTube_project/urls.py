"""youTube_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from youTube_project import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from youTube_app.views import index_view, results_view, logout_view
from youTube_app.views import login_view, profile_view, update_profile_view
from youTube_app.views import reset_request_view, password_reset_view

urlpatterns = [
    path('', index_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/<str:username>/', profile_view, name='profile'),
    path('results/', results_view, name='results'),
    path('updateprofile/<str:username>/',
         update_profile_view, name='update_profile'),
    path('resetrequest/', reset_request_view, name='request_reset'),
    path('passwordReset/<str:username>/<str:snippet>/',
         password_reset_view, name='password_reset'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
