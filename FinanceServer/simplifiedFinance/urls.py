from django.urls import path
from .views import configViews, authViews


urlpatterns = [
    path("isConfigured/", configViews.isConfigured),
    path("configure/", configViews.configure),
    path("getConfiguration/", configViews.getConfig),
    path("login/", authViews.loginToApp),
    path("logout/", authViews.logoutFromApp),
    path("register/", authViews.registerUser),
    path("session/", authViews.sessionInfo),
]