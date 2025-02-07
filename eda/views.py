from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from.models import *

# Create your views here.
def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about_us.html')
def training(request):
    return  render(request, 'trainings.html')


def partners(request):
    partners = Partner.objects.all()
    return render(request, 'partners.html', {'partners': partners})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Training
from .forms import TrainingForm  # Make sure to create a form for Training

# List trainings
def training_list(request):
    trainings = Training.objects.all()
    return render(request, 'trainings.html', {'trainings': trainings})

# Add training

def add_training(request):
        if request.method == 'POST':
            # Get data from the request
            name = request.POST.get('name')
            location = request.POST.get('location')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # Create a new Training object
            training = Training(
                name=name,
                location=location,
                description=description,
                image=image
            )
            training.save()  # Save the training session to the database

            return redirect('trainings')  # Redirect to the training list page

        return render(request, 'add_training.html')


def edit_training(request, pk):
    training = get_object_or_404(Training, id=pk)
    if request.method == 'POST':
        training.name = request.POST.get('name')
        training.location = request.POST.get('location')
        training.description = request.POST.get('description')
        if 'image' in request.FILES:
            training.image = request.FILES['image']
        training.save()
        return redirect('trainings')
    # Render the edit training template with the training object
    return render(request, 'update_training.html', {'training': training})# Delete training
def delete_training(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            training.delete()
            return redirect('trainings')
        return render(request, 'trainings/delete_training.html', {'training': training})
    return redirect('trainings')



def training_detail(request, training_id):
    # Retrieve the training session by ID
    training = get_object_or_404(Training, id=training_id)
    return render(request, 'training_detail.html', {'training': training})


def add_partner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        partner = Partner(name=name, description=description, image=image)
        partner.save()
        return redirect('partners')
    return render(request, 'add_partner.html')


def edit_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)

    if request.method == 'POST':
        partner.name = request.POST.get('name')
        partner.description = request.POST.get('description')
        image = request.FILES.get('image')

        if image:  # Only update the image if a new one is uploaded
            partner.image = image

        partner.save()
        return redirect('partners')  # Redirect to the partners list view

    return render(request, 'edit_partner.html', {'partner': partner})


def delete_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    if partner:
        partner.delete()
        return redirect('partners')
    return redirect('partners')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to a home page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')




def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.filter(project_type=project.project_type).exclude(id=project.pk)[:3]
    return render(request, 'project_detail.html', {'project': project,'related_projects': related_projects})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'confirm_delete.html', {'project': project})


def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        project_type = request.POST.get('project_type')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')

        if name and project_type and description:
            project = Project(name=name, project_type=project_type, description=description)

            if image_file:
                project.image = image_file
            project.save()
            return redirect('projects')
        else:
            # Handle the case where required fields are missing
            return render(request, 'add_project.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'add_project.html')


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        project_type = request.POST.get('project_type')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')

        if name and project_type and description:
            project.name = name
            project.project_type = project_type
            project.description = description

            if image_file:
                project.image = image_file

            project.save()
            return redirect('projects')
        else:
            # Handle the case where required fields are missing
            return render(request, 'edit_project.html', {'project': project, 'error': 'All fields are required.'})
    else:
        return render(request, 'edit_project.html', {'project': project})

