from django.urls import path
from .views import (configViews,
                    authViews,
                    accountViews,
                    vendorsViews,
                    projectViews,
                    invoiceViews,
                    transactionViews,
                    importExportViews,
                    raportsViews,
                    returnViews)


urlpatterns = [
    path('accounts/', accountViews.getAccounts, name='getAccounts'),
    path('createAccount/', accountViews.createAccount, name='createAccount'),
    path('deleteAccount/<str:name>/', accountViews.deleteAccount, name='deleteAccount'),
    path('login/', authViews.loginToApp, name='loginToApp'),
    path('logout/', authViews.logoutFromApp, name='logoutFromApp'),
    path('register/', authViews.registerUser, name='registerUser'),
    path('sessionInfo/', authViews.sessionInfo, name='sessionInfo'),
    path('users/', authViews.getUsers, name='getUsers'),
    path('isSuperuser/', authViews.isSuperuser, name='isSuperuser'),
    path('permissions/', authViews.getPermissions, name='getPermissions'),
    path('allPermissions/', authViews.getAllPermissions, name='getAllPermissions'),
    path('givePermission/', authViews.givePermission, name='givePermission'),
    path('removePermission/<str:user>/<str:project>', authViews.removePermission, name='removePermission'),
    path("isConfigured/", configViews.isConfigured, name="isConfigured"),
    path("configure/", configViews.configure, name="configure"),
    path("config/", configViews.getConfig, name="getConfig"),
    path("importProjects/", importExportViews.importProjects, name="importProjects"),
    path("importVendors/", importExportViews.importVendors, name="importVendors"),
    path("importSubAccounts/", importExportViews.importSubAccounts, name="importSubAccounts"),
    path("importTransactions/", importExportViews.importTransactions, name="importTransactions"),
    path("exportProjects/", importExportViews.exportProjects, name="exportProjects"),
    path("exportVendors/", importExportViews.exportVendors, name="exportVendors"),
    path("exportSubAccounts/", importExportViews.exportSubAccounts, name="exportSubAccounts"),
    path("exportTransactions/", importExportViews.exportTransactions, name="exportTransactions"),
    path("downloadInvoice/<str:number>/", invoiceViews.downloadInvoice, name="downloadInvoice"),
    path("invoice/<str:number>/", invoiceViews.getInvoice, name="getInvoice"),
    path("invoices/", invoiceViews.getInvoices, name="getInvoices"),
    path("createInvoice/", invoiceViews.createInvoice, name="createInvoice"),
    path("updateInvoice/<str:number>/", invoiceViews.updateInvoice, name="updateInvoice"),
    path("deleteInvoice/<str:number>/", invoiceViews.deleteInvoice, name="deleteInvoice"),
    path("generateInvoice/", invoiceViews.generateInvoice, name="generateInvoice"),
    path("projects/", projectViews.getProjects, name="getProjects"),
    path("createProject/", projectViews.createProject, name="createProject"),
    path("deleteProject/<str:name>/", projectViews.deleteProject, name="deleteProject"),
    path("endProject/<str:name>/", projectViews.endProject, name="endProject"),
    path("graph/", raportsViews.generateGraph, name="generateGraph"),
    path("returns/", returnViews.getReturns, name="getReturns"),
    path("createReturn/", returnViews.createReturn, name="createReturn"),
    path("deleteReturn/<str:returnId>/", returnViews.deleteReturn, name="deleteReturn"),
    path("transactions/", transactionViews.getTransactions, name="getTransactions"),
    path("createTransactionBasic/", transactionViews.createTransactionBasic, name="createTransactionBasic"),
    path("createTransactionInvoice/", transactionViews.createTransactionWithInvoice, name="createTransactionInvoice"),
    path("createTransactionNewVendor/", transactionViews.createTransactionNewVendor, name="createTransactionNewVendor"),
    path("createTransactionFull/", transactionViews.createTransactionFull, name="createTransactionFull"),
    path("updateTransaction/<str:transactionId>/", transactionViews.updateTransaction, name="updateTransaction"),
    path("deleteTransaction/<str:transactionId>/", transactionViews.deleteTransaction, name="deleteTransaction"),
    path("vendors/", vendorsViews.getVendors, name="getVendors"),
    path("createVendor/", vendorsViews.createVendor, name="createVendor"),
    path("deleteVendor/<str:name>/", vendorsViews.deleteVendor, name="deleteVendor"),
    path("updateVendor/<str:name>/", vendorsViews.updateVendor, name="updateVendor"),
]
