from django.conf.urls import url
from views import get_notification_settings, post_notification_settings

urlpatterns = [
    url(r'^gnotisettings/$', get_notification_settings),
    url(r'^pnotisettings/$', post_notification_settings),
]
