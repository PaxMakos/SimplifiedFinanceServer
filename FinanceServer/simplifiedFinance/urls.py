from django.urls import path
from .views import configViews


urlpatterns = [
    path("isConfigured/", configViews.isConfigured),
    path("configure/", configViews.configure),
    path("getConfiguration/", configViews.getConfig),
]