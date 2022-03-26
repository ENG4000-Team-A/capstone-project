"""ConsoleTracker URL Configuration

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
from ConsoleTrackerApp import views, tasks, InternalSocketListener
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('timer/', views.timer, name='timer'),
                  path('start_timer/<int:id>', views.start_timer, name='start_timer'),
                  path('login/', views.login, name='login'),
                  path('machines/', views.getMachines, name='machines'),
                  path('users/', views.getUsers, name="users")
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# runs the time checking background task at startup
tasks.start_query_daemon()

# run listener in the background for requests from external system
InternalSocketListener.start_listener_daemon()
