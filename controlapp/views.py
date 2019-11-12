from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django import forms
from django.forms import ModelForm
#from itsystems.forms import SystemForm
#from itsystems.forms import HostForm
import json
import re

from .models import ControlService

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Controls index.")
