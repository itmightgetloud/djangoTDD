from django.http import HttpResponse


def home_page(request):
	return HttpResponse('<html><title>To-Do</title></html>')

# Create your views here.
