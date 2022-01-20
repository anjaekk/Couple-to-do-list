from django.urls import path, include

from .views import CreateTaskView


urlpatterns = [
    path("task", CreateTaskView.as_view(), name="task"),
]