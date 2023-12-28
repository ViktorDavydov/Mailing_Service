from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/article/<slug>', BlogDetailView.as_view(), name='article'),

]
