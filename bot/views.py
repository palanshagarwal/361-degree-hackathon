from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

def ping(request):
	data={"ok":True}
	return JsonResponse(data)
