from django.conf.urls import url

from views import get_feedback_category, post_feedback_category, get_user_feedback, enable_disable_feedback
from views import post_user_feedback, acknowledge_feedback

urlpatterns = [
    url(r'^getfeedbackcatgry/$', get_feedback_category),
    url(r'^postfeedbackcatgry/$', post_feedback_category),
    url(r'^getfeedback/$', get_user_feedback),
    url(r'^postfeedback/$', post_user_feedback),
    url(r'^enablefeedback/$', enable_disable_feedback),
    url(r'^ackfeedback/$', acknowledge_feedback),
]
