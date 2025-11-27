from django.urls import path
from .views import analyze, upload_dataset

urlpatterns = [
    path('analyze/', analyze, name='analyze'),
    path('upload/', upload_dataset, name='upload_dataset'),
]
