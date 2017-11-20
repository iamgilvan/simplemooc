from django.contrib import admin
from .models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	"""docstring for CourseAdmin"""
	list_display  = ['name', 'slug', 'start_date', 'update_at']
	search_fields = ['name', 'slug']	

admin.site.register(Course, CourseAdmin)
