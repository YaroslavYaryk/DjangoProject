"""menu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
# from icon.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from menu import settings
from django.contrib.auth import views as auth_views
from icon.views import *
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path("", include("icon.urls", namespace="")),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("accounts/password_reset_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("sign_in/",(LoginUser.as_view()), name="sign_in"),
    path("register/",( RegisterUser.as_view()), name="register"),
    path("logout/<slug:admin_name>", LogoutUser.as_view(), name="logout"),
    
    path('accounts/password_change/', PasswordChangeView.as_view(
          template_name='registration/password_change_form.html'),
          name='password_change'),
    path('accounts/password_change/done/',
          PasswordChangeDoneView.as_view(
          template_name='registration/password_change_done.html'),
          name='password_change_done'),
    path("send_feedback/", send_feedback, name="send_feedback"), 
    path("cookie/", setcookie, name = "set_cookie"),   
    path("send_mail_register/", send_mail_register, name="send_mail_register"),
    path("know_more/", know_more, name="know_more"),

    path('', include('social_django.urls', namespace='social')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('captchas/', include('captcha.urls')),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if  settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path(' static/<path:path>', never_cache(serve)))

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns() 


handler404 = "icon.views.handle_not_found"
handler500 = "icon.views.handle_server_error"
handler400 = "icon.views.handle_url_error"
handler403 = "icon.views.handler_forbiden"
