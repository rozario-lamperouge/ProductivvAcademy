from django.urls import path, re_path
from . import views
from events.views import EventListView, EventDetailView

app_name = "events"

urlpatterns = [
    path('',EventListView.as_view(), name='event_list'),
    re_path('detail/(?P<event_id>\d+.*)/', EventDetailView.as_view(),
            name='event_detail'),
]
