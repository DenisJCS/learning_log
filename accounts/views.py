from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """Register new user"""
    if request.method !='POST':
        #Output empty form
        form = UserCreationForm()
    else:
        # Proccesing filled form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log in and redirecting to home page
            login(request, new_user)
            return redirect('learning_logs:index')
    
    #Show empty page
    context = {'form':form}
    return render(request, 'registration/register.html', context)
