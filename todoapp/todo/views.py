from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


from django.core.mail import send_mail
# Create your views here.

@login_required(login_url='/login')
def home(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description']
        )
        return redirect('home')

    tasks = Task.objects.filter(user=request.user).order_by('-complete')
    return render(request, 'home.html', {'tasks': tasks})
@login_required(login_url='/login')
def user_logout(request):
    if request.method == 'POST':
        # Get user and their tasks
        user = request.user
        tasks = Task.objects.filter(user=user).order_by('-complete')

        # Render email template
        subject = 'Your Task Summary from To-Do App'
        message = render_to_string('email/task_summary.html', {
            'user': user,
            'tasks': tasks
        })

        # Send the email
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.content_subtype = 'html'  # For HTML email
        email.send()

        # Logout after sending
        logout(request)
        return redirect('login')

    return render(request, 'home.html')
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
            redirect('login')
    else:
        return render(request, 'login.html')


from .forms import CustomUserCreationForm

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def toggle_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.complete = not task.complete
    task.save()
    return redirect('home')


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('home')

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.save()
        return redirect('home')

    return render(request, 'edit.html', {'task': task})


