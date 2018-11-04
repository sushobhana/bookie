"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add', views.add_book),
    path('addform', views.add_book_form),
    path('search', views.search),
    path('mybooks', views.mybooks),
    path('owners', views.owners),
    path('request', views.requestbook),
    path('requests', views.requests),
    path('grant', views.grant),
    path('deny', views.deny),
    path('return', views.return_book)
]
