from django.conf.urls import url
from . import views

app_name = "Calendar"
urlpatterns = [
	url(r'^calendar/$', views.CalendarView.as_view(), name = 'calendar'),
	url(r'^event/new/$', views.new_event, name='event_new'),
	url(r'^event/details/(?P<event_id>\d+)/$', views.details, name='details'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.edit_event, name='edit_event'),
	url(r'^event/delete/(?P<event_id>\d+)/$', views.delete_event, name='delete_event'),
	url(r'^event/status/(?P<event_id>\d+)/$', views.status_change, name='change_status'),
]