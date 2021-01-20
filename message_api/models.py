from django.db import models


class Message(models.Model):
	slug = models.SlugField('Slug', unique=True)
	text = models.CharField('Text', max_length=160)
	counter = models.IntegerField('Counter', default=0)
	add_date = models.DateTimeField('Add date', auto_now_add=True)
	change_date = models.DateTimeField('Change date', auto_now=True)

	class Meta:
		verbose_name = 'Message'
		verbose_name_plural = 'Messages'

	def __str__(self):
		return f'Message slug: {self.slug}'
