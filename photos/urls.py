
from django.conf.urls import url

from .views import BotView

urlpatterns = [
    url(r'^bot/(?P<botToken>.+)/$', BotView.as_view(), name='command'),
]