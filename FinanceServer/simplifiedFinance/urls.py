from django.urls import path, include
from .views import configViews, authViews, accountViews


urlpatterns = [
    path("isConfig/", configViews.isConfigured),
    path("config/", configViews.configure),
    path("getConfig/", configViews.getConfig),
    path("login/", authViews.loginToApp),
    path("logout/", authViews.logoutFromApp),
    path("register/", authViews.registerUser),
    path("session/", authViews.sessionInfo),
    path("getPermissions/", authViews.getPermissions),
    path("givePermissions/", authViews.givePermissions),
    path("removePermissions/<str:user>/<str:project>", authViews.removePermissions),
    path("getAccounts/", accountViews.getAccounts),
    path("createAccount/", accountViews.createAccount),
    path("deleteAccount/<str:name>", accountViews.deleteAccount),
]