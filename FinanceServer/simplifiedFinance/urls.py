from django.urls import path
from .views import configViews, authViews


urlpatterns = [
    path("isConfig/", configViews.isConfigured),
    path("config/", configViews.configure),
    path("getConfig/", configViews.getConfig),
    path("login/", authViews.loginToApp),
    path("logout/", authViews.logoutFromApp),
    path("register/", authViews.registerUser),
    path("session/", authViews.sessionInfo),
    path("getPermissions/", authViews.getPermissions),
]