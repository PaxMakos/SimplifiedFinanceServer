from django.urls import path, include
from .views import configViews, authViews, accountViews, vendorsViews, projectViews, invoiceViews, transactionViews


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
    path("getVendors/", vendorsViews.getVendors),
    path("createVendor/", vendorsViews.createVendor),
    path("deleteVendor/<str:name>", vendorsViews.deleteVendor),
    path("updateVendor/<str:name>", vendorsViews.updateVendor),
    path("getProjects/", projectViews.getProjects),
    path("createProject/", projectViews.createProject),
    path("deleteProject/<str:name>", projectViews.deleteProject),
    path("endProject/<str:name>", projectViews.endProject),
    path("downloadInvoice/<str:number>", invoiceViews.downloadInvoice),
    path("getInvoice/<str:number>", invoiceViews.getInvoice),
    path("createInvoice/", invoiceViews.createInvoice),
    path("deleteInvoice/<str:number>", invoiceViews.deleteInvoice),
    path("updateInvoice/<str:number>", invoiceViews.updateInvoice),
    path("getTransactions/", transactionViews.getTransactions),
    path("createTransactionBasic/", transactionViews.createTransactionBasic),
    path("createTransactionWithInvoice/", transactionViews.createTransactionWithInvoice),
    path("createTransactionNewVendor/", transactionViews.createTransactionNewVendor),
    path("deleteTransaction/<int:id>", transactionViews.deleteTransaction),
    path("updateTransaction/<int:id>", transactionViews.updateTransaction),

]