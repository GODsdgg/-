from django.conf.urls import url
from . import views

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    #/users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterPhoneCountAPIView.as_view(), name='phonecount'),
    url(r'^$',views.RegisterCreateUserView.as_view()),

    # 定义url
    url(r'^auths/', obtain_jwt_token),

    # /users/infos/
    url(r'^infos/$',views.UserCenterView.as_view()),

    url(r'^emails/$',views.UserEmailView.as_view()),



]

"""
header:     eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
payload:    eyJlbWFpbCI6IiIsInVzZXJfaWQiOjQsInVzZXJuYW1lIjoicXdlcnR0IiwiZXhwIjoxNTQxNTgwMzU4fQ.
signature:  wTMfs62193U02Bj-JCRLytH6LiCAcw8nympOGZgGvwU
"""




