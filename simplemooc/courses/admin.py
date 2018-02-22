from django.contrib import admin
from .models import Course, Enrollment, Announcement, Comment, Lesson, Material

# Register your models here.
# Personalise seu admin aqui
class CourseAdmin(admin.ModelAdmin):
	list_display        = ['name', 'slug', 'start_date', 'updated_at']
	search_fields       = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

class MaterialAdmin(admin.StackedInline):
	model = Material

class LessonAdmin(admin.ModelAdmin):
	list_display  = ['name', 'number', 'course', 'release_date']
	search_fields = ['name', 'description']
	list_filter   = ['created_at']

	inline = [MaterialAdmin]

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)