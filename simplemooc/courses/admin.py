from django.contrib import admin
from .models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	"""docstring for CourseAdmin"""
	list_display       = ['name', 'slug', 'start_date', 'update_at']
	search_fields      = ['name', 'slug']	
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Course, CourseAdmin)
