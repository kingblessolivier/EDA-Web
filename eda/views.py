
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth.hashers import make_password


def index(request):
    projects = Project.objects.all()[:3]
    partners = Partner.objects.all()[:4]
    trainings = Training.objects.filter()[:3]
    images=gallery.objects.all()
    programs=Programs.objects.all()[:3]
    return render(request, 'home.html', {'projects': projects, 'partners': partners, 'trainings': trainings, 'images':images, 'programs':programs})



def about(request):
    members=Team.objects.all()
    context = {'members': members}
    return render(request, 'about_us.html', context)
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


def terms_and_conditions(request):
    return render(request, 'terms_of_service.html')


def privacy_policy(request):
    return render(request, 'privacy.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('reset_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('reset_password')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('reset_password')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Important to update the session with the new password
        messages.success(request, 'Your password has been successfully reset.')
        return redirect('login')

    return render(request, 'reset_password.html')





# profile view
@login_required
def profile(request):
    return render(request, 'profile.html')


# ✅ 1. Retrieve All Users (JSON Response)
class UserListView(ListView):
    model = User

    def render_to_response(self, context, **response_kwargs):
        users = list(self.model.objects.values('id', 'username', 'email', 'first_name', 'last_name'))
        return JsonResponse(users, safe=False)


@login_required
def user_detail_view(request):
    user = request.user  # Get the currently logged-in user
    if user.is_authenticated:
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)


@login_required
@csrf_exempt
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'DELETE':
        if request.user.is_superuser:
            user.delete()
            return JsonResponse({"message": "User deleted successfully!"})
        return JsonResponse({"error": "You don't have permission to delete this user."}, status=403)
    return JsonResponse({"error": "Method not allowed"}, status=405)


# ✅ 3. Add New User (Handled via JavaScript, returns JSON)
class UserCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Parse JSON data from request
            username = data.get('username')
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            password = data.get('password')

            # Check if required fields are provided
            if not username or not password:
                return JsonResponse({"error": "Username and password are required."}, status=400)

            # Create user
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password)  # Hash the password
            )

            return JsonResponse({"message": "User added successfully!", "user_id": user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)


# ✅ 4. Update User (JSON Response, handled via JavaScript)
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']

    def form_valid(self, form):
        user = form.save()
        return JsonResponse({"message": "User updated successfully!"})

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)


# Adding team member
@csrf_exempt
def add_team_member(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            designation = request.POST.get('designation')
            image = request.FILES.get('image')  # Get the uploaded image

            team_member = Team.objects.create(name=name, designation=designation, image=image)

            return JsonResponse({'message': 'Team member added successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Return error details

    return JsonResponse({'error': 'Invalid request method'}, status=405)


class TeamListView(ListView):
    model = Team

    def render_to_response(self, context, **response_kwargs):
        member = list(self.model.objects.values('id', 'name', 'designation', 'image'))
        return JsonResponse(member, safe=False)


def user_detail(request, pk):  # pk comes from the URL
    try:
        user = User.objects.get(pk=pk)
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def customer_messages(request):
    messages= Contact.objects.all()
    subscribers=Subscribe.objects.all()
    return render(request, 'customer_messages.html', {'messages': messages,'subscribers': subscribers})


def delete_message(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    if message:
        message.delete()
        return redirect('customer_messages')
    return redirect('customer_messages')

def add_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            return redirect('about')
        else:
            return render(request, 'about_us.html', {'error': 'All fields are required.'})
    return render(request, 'about_us.html')


@csrf_exempt
@login_required
def delete_team_member(request, pk):
    member = get_object_or_404(Team, pk=pk)
    if request.method == 'DELETE':
        if request.user.is_superuser:
            member.delete()
            return JsonResponse({"message": "Team member deleted successfully!"})
        return JsonResponse({"error": "You don't have permission to delete this team member."}, status=403)
    return JsonResponse({"error": "Method not allowed"}, status=405)



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)


def add_gallery(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')

        if name and image:
            gallery.objects.create(name=name, image=image)
            return redirect('gallery')  # Redirect to the gallery page or wherever you like

    return render(request, 'add_image.html')


def delete_gallery(request, pk):
    galler = get_object_or_404(gallery, pk=pk)
    if request.method == 'POST':
        galler.delete()
        return redirect('gallery')




def galleryView(request):
    galleries = gallery.objects.all()
    return render(request, 'gallery.html', {'galleries': galleries})


def edit_gallery(request, pk):
    galle = get_object_or_404(gallery, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name and image:
            galle.name = name
            galle.image = image
            galle.save()
            return redirect('gallery')
        return render(request, 'edit_galler.html', {'galle': galle})
    return render(request, 'edit_galley.html', {'galle': galle})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            sub = Subscribe(email=email)
            sub.save()
            messages.success(request, 'You have successfully subscribed to our newsletter.')
            return redirect('index')
        else:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('index')
    return render(request,'home.html')

def unsubscribe(request, pk):
    sub = get_object_or_404(Subscribe, pk=pk)
    if sub:
        sub.delete()
        messages.success(request, 'You have successfully unsubscribed from our newsletter.')
        return redirect('customer_messages')
    return redirect('customer_messages')


def programs_view(request):
    programs = Programs.objects.all()  # Fetch all programs
    return render(request, 'programs.html', {
        'programs': programs,
    })


def add_program_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        program = Programs(name=name, description=description, image=image)
        program.save()

        return redirect('programs')  # Redirect to the programs list after saving

    return render(request, 'add_program.html')


def update_program_view(request, program_id):
    program = get_object_or_404(Programs, id=program_id)

    if request.method == 'POST':
        program.name = request.POST.get('name')
        program.description = request.POST.get('description')
        image = request.FILES.get('image')

        if image:
            program.image = image
        program.save()

        return redirect('programs')  # Redirect to the programs list after updating

    return render(request, 'update_program.html', {
        'program': program,
    })


def delete_program_view(request, program_id):
    program = get_object_or_404(Programs, id=program_id)
    program.delete()
    return redirect('programs')  # Redirect to the programs list after deletion


def program_detail_view(request, program_id):
    program = get_object_or_404(Programs, id=program_id)
    return render(request, 'program_detail.html', {
        'program': program,
    })
