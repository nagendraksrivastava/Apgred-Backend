from django.conf.urls import url
from auth import login_user, logout_user, business_lead, reset_password, signup_user
from views import total_user, get_active_user_count
from versions import get_all_versions, request_update, add_new_version

urlpatterns = [
    url(r'^login/$', login_user),
    url(r'^logout/$', logout_user),
    url(r'^businesslead/$', business_lead),
    url(r'^resetpwd/$', reset_password),
    url(r'^signup/$', signup_user),
    url(r'^totaluser/$', total_user),
    url(r'^activeuser/', get_active_user_count),
    url(r'^appuser/', get_active_user_count),
    url(r'^allversion/', get_all_versions),
    url(r'^appupdate/', request_update),
    url(r'^addversion/', add_new_version),
]
