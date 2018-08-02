from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^register/$', register_device),
    url(r'^validateclient/$', validate_client),
    url(r'^softupdatecancel/$', soft_update_cancel),
    url(r'^softupdate/$', soft_push_ok_click),
    url(r'^hardupdate/$', hard_push_ok_click),
    url(r'^forceupdate/$', get_forceupdate),
]
