"""unn_csr_workplace_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from unn_csr_workplace_py import views

urlpatterns = [
    path('customer/<int:customer_id>/service/<int:service_id>/broken', views.service_is_broken, name='broke the service'),
    path('customer/<int:customer_id>/service/<int:service_id>', views.service_details, name='service_details'),
    path('customer/<int:customer_id>', views.customer_details, name='customer_details'),
    path('customer/', views.customer_search, name='search'),
    path('admin/', admin.site.urls),
    path('', views.to_customer_search)
]
