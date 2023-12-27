from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import Registration, Log_in, Change_pass, Player
from .models import User, RoomCode, JoinedRoom
from django import forms

from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
import random


EMAIL_HOST = 'dreameralex9@gmail.com'

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'tictactoe/password_reset.html'
    email_template_name = 'tictactoe/password_reset_email.html'
    subject_template_name = 'tictactoe/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


def index(request):
    if request.user.is_authenticated:
        # When user enters the page, the previous created room or joined room should be deleted
        created_room = RoomCode.objects.filter(user=request.user)
        joined_room = JoinedRoom.objects.filter(joiner=request.user)
        if created_room:
            created_room.delete()
        if joined_room:
            joined_room.delete()

    return render(request, 'tictactoe/index.html')
    



def register(request):
    if request.method == 'POST':
        # Call the class Registration to access the form data
        form = Registration(request.POST)

        # Check if the form submition is valid
        if form.is_valid():
            # Access to all filled forms
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['confirmation']

            # Email existance checking
            if User.objects.filter(email=email):
                form = Registration()
                # Creating error message
                messages.error(request, "User with this email already existed")
                return render(request, 'tictactoe/sign_in.html', {
                    'form': form
                })

            # Password validation checking by django build in validations
            # try: 
            #     validate_password(password)
            # except forms.ValidationError as error:
            #     form = Registration()
            #     # Joining the error list to one string error
            #     errors = ' '.join(error)
            #     # Creating error message to the user
            #     messages.error(request, errors)
            #     return render(request, 'tictactoe/sign_in.html', {
            #         'form': form
            #     })
            
            # Check password configuration
            if password != confirmation:
                form = Registration()
                messages.error(request, "Passwords must match.")
                return render(request, 'tictactoe/sign_in.html', {
                    'form': form
                })

            # Saving the signed in user into the database
            try:
                user = User.objects.create_user(username, email, password)
                user.save
            except IntegrityError: # Checking about user existance
                form = Registration()
                messages.error(request, "Username already exists.")
                return render(request, 'tictactoe/sign_in.html', {
                    'form': form
                })

            # Logging in the user; after signing in
            login(request, user)

            # Rendering to the index page with a success message
            messages.success(request, "You are signed in successfully.")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = Registration()
        return render(request, 'tictactoe/sign_in.html', {
            "form": form
        })


def message(request): 
    # This rout is for log in url
    messages.error(request, "You have to log/ sign in first.")
    return HttpResponseRedirect(reverse("register"))


# Log in page
def log_in(request):
    if request.method == "POST":
        # Accessing to the created form
        form = Log_in(request.POST)

        # Checking form validation
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None: # Authentication success; loggin in
                login(request, user)
                print('this is your email: ')
                print(request.user.email)
                messages.success(request, "You are logged in successfully.")
                return HttpResponseRedirect(reverse("index"))
            else:
                form = Log_in()
                messages.error(request, "Invalid username and/ or password")
                return render(request, 'tictactoe/log_in.html', {
                    'form': form
                })
    else:
        form = Log_in()
        return render(request, 'tictactoe/log_in.html', {
            'form': form
        })
    

@login_required
def log_out(request):
    # When user enters the page, the previous created room or joined room should be deleted
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    if created_room:
        created_room.delete()
    if joined_room:
        joined_room.delete()

    # Logging out the user
    logout(request)
    messages.success(request, "You are logged out successfully.")
    return HttpResponseRedirect(reverse("index"))


@login_required
def change_password(request):
    if request.method == "POST":
        # Accessing to the form
        form = Change_pass(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            new_password_conf = form.cleaned_data['new_pass_conf']

            # User password authentication
            username = request.user.username
            user = authenticate(request, username=username, password=current_password)
            if user is None:
                form = Change_pass()
                messages.error(request, "Invalid Password.")
                return render(request, 'tictactoe/change_pass.html', {
                    'form': form
                })

            # New password validation by django build in password validation
            try:
                validate_password(new_password)
            except forms.ValidationError as error:
                form = Change_pass()
                # Joining the error list to one string error
                errors = ' '.join(error)
                # Creating error message to the user
                messages.error(request, errors)
                return render(request, 'tictactoe/change_pass.html', {
                    'form': form
                })

            # New password confirmation
            if new_password != new_password_conf:
                form = Change_pass()
                messages.error(request, "New password must match.")
                return render(request, 'tictactoe/change_pass.html', {
                    'form': form
                })

            # Password update
            usr = User.objects.get(username=username)
            usr.set_password(new_password)
            usr.save()

            # Logging in user with new password
            login(request, usr)
            messages.success(request, "Your password has changed successfully.")
            return HttpResponseRedirect(reverse("index"))

    else:
        form = Change_pass()
        return render(request, "tictactoe/change_pass.html", {
            'form': form
        })

@login_required
def enter(request):
    # When user enters the page, the previous created room or joined room should be deleted
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    if created_room:
        created_room.delete()
    if joined_room:
        joined_room.delete()
    
    return render(request, "tictactoe/enter.html")


@login_required
def create_room(request):
    # When user enters the page, the previous created room or joined room should be deleted
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    if created_room:
        created_room.delete()
    if joined_room:
        joined_room.delete()
        
    # Generate 6 digit random numbers 
    room_code = random.randint(100000, 999999)

    # For now save the code in database
    RoomCode.objects.create(user=request.user, room_code=str(room_code))

    return render(request, 'tictactoe/create.html', {
        'code': room_code
    })


@login_required
def join_room(request):
    # When user enters the page, the previous created room or joined room should be deleted
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    if created_room:
        created_room.delete()
    if joined_room:
        joined_room.delete()

    # Creating an input for entering the room number
    if request.method == 'POST':
        join_code = request.POST['room_code']

        # Check that is it a valid room code 
        code = RoomCode.objects.filter(room_code=join_code)
        if code:
            # Check whether this code is a used code or not
            used_code = JoinedRoom.objects.filter(joined=join_code)
            if used_code:
                messages.error(request, "This code is already in use. Please enter new room code.")
                return render(request, 'tictactoe/join.html')
            
            # Save the success result to database
            JoinedRoom.objects.create(joiner=request.user, joined=join_code)
            messages.success(request, "Room is successfully joined.")
            return HttpResponseRedirect(reverse('room'))
        else:
            messages.error(request, 'Join code is not existed. Please enter the code carefully.')
            return render(request, 'tictactoe/join.html')
    else:
        return render(request, 'tictactoe/join.html')


@login_required
def room(request):
    # Prevent entering users without any creating room or joining room process
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    
    if created_room:
        return render(request, 'tictactoe/room.html', {
            'created_room': created_room[0].room_code
        })
    if joined_room:
        return render(request, 'tictactoe/room.html', {
            'created_room': joined_room[0].joined
        })
    return HttpResponseRedirect(reverse('enter'))
    

@login_required
def computer(request):
    if request.method == "POST":
        # Create the form and access the submitted data
        form = Player(request.POST)
        player = request.POST['player_as']
        # Render to the playing page
        return render(request, 'tictactoe/tictactoe.html', {
            'player': player
        })
    else:
        form = Player()
        return render(request, 'tictactoe/play_as.html', {
            'form': form
        })

@login_required
def about_contact(request):
    return render(request, 'tictactoe/about_contact.html')

@csrf_exempt
@login_required
def is_joined(request):
    # Check whether another user joined created room or not
    my_code = RoomCode.objects.filter(user=request.user)
    if not my_code:
        return JsonResponse({'connected': False})
    
    joined_person = JoinedRoom.objects.filter(joined=my_code[0].room_code)
    if not joined_person:
        return JsonResponse({'connected': False})
    
    return JsonResponse({'connected': True})


@csrf_exempt
@login_required
def cur_usr(request):
    # Return the current user data; logged in user
    current_user = User.objects.get(id=request.user.id)
    return JsonResponse({'id': current_user.id, 'name': current_user.username})


@csrf_exempt
@login_required
def delete_current_connection(request):
    # When user enters the page, the previous created room or joined room should be deleted
    created_room = RoomCode.objects.filter(user=request.user)
    joined_room = JoinedRoom.objects.filter(joiner=request.user)
    if created_room:
        created_room.delete()
    if joined_room:
        joined_room.delete()
    return JsonResponse({"message": "The previous connections removed successfully."})



