"""poll URL Configuration

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


from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('surveys/create_survey/', views.create_survey),
    path('surveys/delete/', views.delete_survey),
    path('surveys/set_survey_date/', views.set_survey_date),
    path('update_survey/', views.update_survey),
    path('surveys/active', views.get_active_surveys),
    path('surveys/start/<survey_name>/', views.start_survey),
    path('surveys/add/', views.add_question),
    path('surveys/completed', views.get_completed_surveys),
    path('surveys/<survey_name>/', views.get_answers),
    path('<survey_name>/complete', views.complete_survey),
    path('survey/write/', views.write_answer),
]
