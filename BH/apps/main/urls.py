from django.urls import re_path
from apps.main import views

app_name="main"

urlpatterns = [
    re_path(r"insert_data/",views.InsertDataFromExcel.as_view()),
]