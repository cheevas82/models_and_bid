from django.views import View	
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import	authenticate, login
from .forms import UserCreationForm

class Register(View):

	template_name = 'registration/register.html'

	def get(self, request):
		context = {
			'form': UserCreationForm()
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			# username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=password)
			login(request, user)
			return redirect('home')
		context = {
			'form': form
		}
		return render(request, self.template_name, context)