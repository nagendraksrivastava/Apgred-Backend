from django.conf.urls import url
from auth import login_user, logout_user, business_lead, reset_password, signup_user
from views import total_user, app_users

urlpatterns = [
    url(r'^login/$', login_user),
    url(r'^logout/$', logout_user),
    url(r'^businesslead/$', business_lead),
    url(r'^resetpwd/$', reset_password),
    url(r'^signup/$', signup_user),
    url(r'^totaluser/$', total_user),
    url(r'^activeuser/', app_users),
]
