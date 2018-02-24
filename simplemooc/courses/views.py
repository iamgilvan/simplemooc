from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

def index(request):
    courses       = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)

# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     context = {
#         'course': course
#     }
#     template_name = 'courses/details.html'
#     return render(request, template_name, context)

def details(request, slug):
    course  = get_object_or_404(Course, slug=slug)
    context = {}
    #valid form?
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data)
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['course'] = course
    context['form']   = form
    template_name     = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course              = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user= request.user, course=course
    )
    if created:
        enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course     = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    tamplate = 'courses/announcements.html'
    context  = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, tamplate, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    #Obter anuncio do curso relacionado
    announcement = get_object_or_404(course.announcements.all(), pk=pk)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        #No save on database, return only the object
        comment      = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Sua mensagem foi enviada com sucesso')

    tamplate = 'courses/show_announcement.html'
    context  = {
        'course': course,
        'announcement': announcement,
        'form':form,
    }
    return render(request, tamplate, context)
