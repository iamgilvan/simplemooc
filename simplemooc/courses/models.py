from django.db import models
from django.conf import settings

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
	description = models.TextField('Simple Description', blank=True)
	about       = models.TextField('About the Course', blank=True)
	start_date  = models.DateField('Start Date', null=True, blank=True)
	image       = models.ImageField(upload_to='courses/image', verbose_name='Image', null=True, blank=True)
	create_at   = models.DateTimeField('Create in ', auto_now_add=True)
	update_at   = models.DateTimeField('Update in ', auto_now=True)
	objects     = CourseManager()

	def __str__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
    	#from django.core.urlresolvers import reverse
		#return reverse('', kwargs={'pk': self.pk})
		return ('courses:details', (), {'slug': self.slug})

	class Meta:
		"""docstring for Meta"""
		verbose_name        = 'Course'
		verbose_name_plural = 'Courses'
		ordering            = ['name']
			
class Enrollment(models.Model):
	STATUS_CHOICES  = (
		(0, 'Pendant'),
		(1, 'Approved'),
		(2, 'Canceled'),
	)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='User', related_name='enrollments'
	)

	course = models.ForeignKey(
		Course, verbose_name='Course', related_name='enrollments'
	)

	status = models.IntegerField(
		'Situation', choices=STATUS_CHOICES, default=0, blank=True
	)

	create_at   = models.DateTimeField('Create in ', auto_now_add=True)
	update_at   = models.DateTimeField('Update in ', auto_now=True)

	#ativar o aluno
	def active(self):
		self.status = 1
		self.save()

	class Meta:
		verbose_name        = 'Enrollment'
		verbose_name_plural = 'Enrollments'
		unique_together     = (('user', 'course'),)