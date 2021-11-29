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
from django.contrib import admin
from django.urls import path
from ConsoleTrackerApp import views
from django.conf import settings
from django.conf.urls.static import static
from ConsoleTrackerApp import tasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('time_manager/<int:id>', views.time_manager, name = 'time_manager'),
    path('timer/<int:id>', views.timer, name = 'timer'),
    path('login/', views.login, name = 'login'),
    path('machines/', views.machines.as_view(), name='machines'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# runs the time checking background task at startup
tasks.main()
