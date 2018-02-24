from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template

# Create your models here.
class CourseManager(models.Manager):
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
	created_at  = models.DateTimeField('Create in ', auto_now_add=True)
	updated_at  = models.DateTimeField('Update in ', auto_now=True)
	objects     = CourseManager()

	def __str__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
    	#from django.core.urlresolvers import reverse
		#return reverse('', kwargs={'pk': self.pk})
		return ('courses:details', (), {'slug': self.slug})

	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__gte=today)


	class Meta:
		"""docstring for Meta"""
		verbose_name        = 'Course'
		verbose_name_plural = 'Courses'
		ordering            = ['name']

class Lesson(models.Model):

	name        = models.CharField('Name', max_length = 100)
	description = models.TextField('Description', blank=True)
	number      = models.IntegerField('Number (order)', blank=True, default=0) # Definir ordem das aulas
	release_date= models.DateField('Date avaliable', blank=True, null=True)

	#Relação com o curso
	course      = models.ForeignKey(Course, verbose_name='Course', related_name='lessons')

	created_at  = models.DateTimeField('Create in ', auto_now_add=True)
	updated_at  = models.DateTimeField('Update in ', auto_now=True)

	def __str__(self):
		return self.name

	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today
		return False

	class Meta:
		verbose_name 		= "Lesson"
		verbose_name_plural = "Lessons"
		ordering            = ['number']

class Material(models.Model):

	name        = models.CharField('Name', max_length = 100)
	embedded    = models.TextField('Video embedded', blank=True)
	file        = models.FileField(upload_to='lessons/materials', blank=True, null=True)

	lesson      = models.ForeignKey(Lesson, verbose_name='Lesson',related_name='materials')

	def is_embedded(self):
		return bool(self.embedded)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name        = "Material"
		verbose_name_plural = "Materials"

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

	created_at   = models.DateTimeField('Create in ', auto_now_add=True)
	updated_at   = models.DateTimeField('Update in ', auto_now=True)

	#ativar o aluno
	def active(self):
		self.status = 1
		self.save()

	#check status do curso
	def is_approved(self):
		return self.status == 1

	class Meta:
		verbose_name        = 'Enrollment'
		verbose_name_plural = 'Enrollments'
		unique_together     = (('user', 'course'),)

# Anúncios do curso
class Announcement(models.Model):
	course = models.ForeignKey(Course, verbose_name='course',related_name='announcements')
	title  = models.CharField('Title', max_length=100)
	content= models.TextField('Content')

	created_at   = models.DateTimeField('Create in ', auto_now_add=True)
	updated_at   = models.DateTimeField('Update in ', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name        = 'Announcement'
		verbose_name_plural = 'Announcements'
		ordering            = ['-created_at']

# Comentários do curso
class Comment(models.Model):
	announcement = models.ForeignKey(Announcement, verbose_name='Announcement', related_name='comments')
	user         = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user')
	comment      = models.TextField('Comments')


	created_at   = models.DateTimeField('Create in ', auto_now_add=True)
	updated_at   = models.DateTimeField('Update in ', auto_now=True)

	class Meta:
		verbose_name        = 'Comment'
		verbose_name_plural = 'Comments'
		ordering            = ['created_at']

def post_save_announcement(instance, created, **kwargs):
	if created:
		subject = instance.title
		context = {
			'announcement':instance
		}
		template_name = 'courses/announcements_mail.html'
		#Obter email dos usuários
		enrollments = Enrollment.objects.filter(course=instance.course, status=1)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)

#Signal a ser disparado para um novo anúncios
models.signals.post_save.connect(post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement')