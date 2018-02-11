from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course
from .models import Enrollment
from .forms import ContactCourse

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
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    #Checar se usuário está inscrito no curso
    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment,  user= request.user, course=course)
        if not enrollment.is_approved():
            messages.error(request, "A sua inscrição está pendente")
            return redirect('accounts:dashboard')
    tamplate = 'courses/announcements.html'
    context  = {
        'course': course
    }
    return render(request, tamplate, context)