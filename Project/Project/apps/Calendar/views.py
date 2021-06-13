from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm


class CalendarView(generic.ListView):
	model = Event
	template_name = 'Calendar/calendar.html'

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		date = get_date(self.request.GET.get('month', None))

		cal = Calendar(date.year, date.month)

		html_cal = cal.formatmonth(withyear=True)
		context['calendar'] = mark_safe(html_cal)

		date = get_date(self.request.GET.get('month', None))
		context['prev_month'] = prev_month(date)
		context['next_month'] = next_month(date)
		return context




def get_date(required_month):
	if required_month:
		year, month = (int(x) for x in required_month.split('-'))
		return date(year, month, day = 1)
	return datetime.today()


def prev_month(current_month):
	first = current_month.replace(day=1)
	prev_month = first - timedelta(days=1)
	month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
	return month


def next_month(current_month):
	days_in_month = calendar.monthrange(current_month.year, current_month.month)[1]
	last = current_month.replace(day=days_in_month)
	next_month = last + timedelta(days=1)
	month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
	return month


def details(request, event_id):
 	choosenEvent = Event.objects.get(id = event_id)
 	return render(request, 'Calendar/details.html', {'choosenEvent':choosenEvent})


def new_event(request):
    instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('Calendar:calendar'))
    return render(request, 'Calendar/event.html', {'form': form})


def edit_event(request, event_id=None):
	instance = Event()
	if event_id:
		instance = get_object_or_404(Event, pk=event_id)
	form = EventForm(request.POST or None, instance=instance)
	if request.POST and form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('Calendar:details', args=(event_id,)))
	return render(request, 'Calendar/event.html', {'form':form})

def delete_event(request, event_id):
	event_to_delete = Event.objects.get(id = event_id)
	event_to_delete.delete()
	return HttpResponseRedirect(reverse('Calendar:calendar'))




