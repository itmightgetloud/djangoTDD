from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from accounts.models import Token
from django.core.urlresolvers import reverse

def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token=' + str(token.uid)
	)
	message_body = f'Use this link to log in:\n\n{url}'
	send_mail(
		'Your login link for Todo app', 
		message_body,
		'noreply@todoapp', 
		[email]
	)
	messages.success(
		request,
		"Check your email for activation link."
	)
	return redirect('/')

def login(request):
	user = auth.authenticate(uid=request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')



# Create your views here.
