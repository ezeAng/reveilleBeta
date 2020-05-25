from django.shortcuts import render

# Create your views here.
def home(request):
	context = {
		'posts': posts
	}
	return render(request, 'attendance/revhome.html/', context)

def admin(request):
	return render(request, 'attendance/revadmin.html/')
