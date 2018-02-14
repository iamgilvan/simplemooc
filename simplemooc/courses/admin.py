from django.contrib import admin
from .models import Course, Enrollment, Announcement, Comment

# Register your models here.
# Personalise seu admin aqui
class CourseAdmin(admin.ModelAdmin):
	"""docstring for CourseAdmin"""
	list_display       = ['name', 'slug', 'start_date', 'updated_at']
	search_fields      = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Course, CourseAdmin)
