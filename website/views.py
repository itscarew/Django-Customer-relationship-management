from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.decorators.cache import never_cache
from .forms import RegisterForm, RecordForm
from .models import Record


# Create your views here.
@never_cache
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, "Sign in successful")
            return redirect("dashboard")
        else: 
            messages.error(request, "Sign in error. Couldn't sign in")
            # Preserve the entered username
            return render(request, 'home.html', {'username': username})
    else: 
       return render(request, 'home.html', {} )

@login_required(login_url='/')
def dashboard(request):
    records = Record.objects.all()
    return render(request, 'dashboard.html', {'records' : records} )

@never_cache
def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registered successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Sign up error. Couldn't sign up")
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('home')

@login_required(login_url='/')
def record(request, pk):
    # Look Up Record
	record = Record.objects.get(id=pk)
	return render(request, 'record.html', {'record': record})

@login_required(login_url='/')
def delete_record(request, pk):
		delete_record = Record.objects.get(id=pk)
		delete_record.delete()
		messages.success(request, "Record Deleted successfully")
		return redirect('dashboard')

@login_required(login_url='/')
def add_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Added successfully")
            return redirect('dashboard')
    else:
        form = RecordForm()
        return render(request, 'add_record.html', {'form': form})

@login_required(login_url='/')
def update_record(request, pk):
		record = Record.objects.get(id=pk)
		form = RecordForm(request.POST or None, instance=record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record updated successfully!")
			return redirect('dashboard')
		return render(request, 'update_record.html', {'form':form})
