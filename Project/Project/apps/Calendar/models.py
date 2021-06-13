from django.db import models
from django.urls import reverse
from datetime import *

class Event(models.Model):
	title = models.CharField(max_length = 200)
	description = models.TextField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	status = models.BooleanField(default=False)

	#Функция возвращает оставшееся время до конца ивента
	def TimeRemains(self):
		remaining_time = self.end_time - datetime.now(timezone.utc)
		expire_check = self.end_time
		#Проверка кол-ва секунд между датой конца события и текущей датой
		if remaining_time.total_seconds() < 0:
			return 'Event expired!'
		return remaining_time

	@property
	def get_html_url(self):
		url = reverse('Calendar:details', args=(self.id,))
		return f'<a href="{url}"> {self.title} </a>'

