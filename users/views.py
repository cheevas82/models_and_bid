from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.views import View
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import UserCreationForm
from .utils import send_email_for_verify
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.tokens import default_token_generator as token_generator


User = get_user_model()

class MyLoginView(LoginView):
	pass


class EmailVerify(View):
	def get(self, request, uidb64, token):
		user = self.get_user(uidb64)

		if user is not None and token_generator.check_token(user, token):
			user.email_verify = True
			user.save()
			login(request, user)
			return redirect('home')
		return redirect('invalid_verify')

	@staticmethod
	def get_user(uidb64):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
			user = None
		return user

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
			send_email_for_verify(request, user)
			return redirect('confirm_email')
			# login(request, user)
			# return redirect('home')
		context = {
			'form': form
		}
		return render(request, self.template_name, context)