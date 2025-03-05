"""
URL configuration for Net_Banking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.conf.urls import handler404
from django.shortcuts import render
from django.urls import path
from Bank import views

def custom_404_view(request, exception):
    return render(request, 'Admin/error404.html', status=404)

handler404 = custom_404_view

urlpatterns = [

    #----------user----------

    path('', views.index),                                #starting url path.
    path('index',views.index),                            #url for index page.
    path('netBanking',views.netBanking),                  #url for netbanking page.
    path('about',views.about),                            #url for about page.
    path('contact',views.contact),                        #url for contact page.
    path('sign-up',views.sign_up),
    path('userIndex',views.user_sign_in),                 #url for sign in button.
    path('logout',views.user_sign_out),                   #url for sign out button.

    #----------admin----------
    
    path('admin/',views.adminindex,name='admin'),                    #starting url path for admin.
    path('admin/dashboard',views.adminlogin),                        #url for admin login.
    path('admin/login',views.adminlogout),                           #url for admin logout.
    path('admin/change-password',views.forgetpass),                  #url for change password page.
    path('admin/home',views.dashboard,name='adminDashboard'),        #url for home/dashbord.
    path('admin/add-account',views.add_account),                     #url for add accounts page.
    path('admin/account-added',views.AddFiles),                      #url for adding new account.  

    #----------captcha----------

    path('captcha/',include('captcha.urls')),

]
