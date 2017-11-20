from django.db import models

# Create your models here.
class CourseManager(models.Manager):
	"""docstring for CourseMamodels.Manager"""
	def Search(self, query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) |
			models.Q(description__icontains=query)
		)

class Course(models.Model):
	
	name        = models.CharField('Name', max_length = 100)
	slug        = models.SlugField('Trigger')
	description = models.TextField('Description', blank=True)
	start_date  = models.DateField('Start Date', null=True, blank=True)
	image       = models.ImageField(upload_to='courses/image', verbose_name='Image', null=True, blank=True)

	create_at   = models.DateTimeField('Create in ', auto_now_add=True)
	update_at   = models.DateTimeField('Update in ', auto_now=True)

	objects = CourseManager()

	def __str__(self):
		return self.name

	class Meta:
		"""docstring for Meta"""
		verbose_name        = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering            = ['name']
			
