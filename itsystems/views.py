from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django import forms
from django.forms import ModelForm
from itsystems.forms import SystemForm
from itsystems.forms import HostForm
from itsystems.forms import AgentForm
from itsystems.forms import AgentServiceForm
from itsystems.forms import ComponentForm
from itsystems.forms import VendorForm
import json

import re

from .models import System, Host, AgentService, Agent, Component, Vendor

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the itsystems index.")

@login_required
def itsystems_home(request):
    """Show content relevant to IT systems"""
    # TODO: Restrict to user's permissions
    return render(request, "itsystems/itsystems_home.html", {
        "systems": System.objects.all(),
    })

@login_required
def system_list(request):
    """List system instances"""
    # TODO: Restrict to user's permissions
    return render(request, "itsystems/system_index.html", {
        "systems": System.objects.all(),
    })

@login_required
def host_list(request):
    """List host instances"""
    # TODO: Restrict to user's permissions
    return render(request, "itsystems/host_index.html", {
        "hosts": Host.objects.all(),
    })

@login_required
def agents_list(request):
    """List host instances"""
    # TODO: Restrict to user's permissions
    return render(request, "itsystems/agent_index.html", {
        "agents": Agent.objects.all(),
    })

@login_required
def system_hosts_list(request, pk):
    """List system instance host intances"""
    # TODO: Restrict to user's permissions
    system  = System.objects.get(id=pk)
    hosts = system.get_hosts()
    return render(request, "itsystems/system_hosts.html", {
        "system": system,
        "hosts": hosts,
    })

@login_required
def components_list(request):
    """List host instances"""
    # TODO: Restrict to user's permissions
    return render(request, "itsystems/component_index.html", {
        "component": Component.objects.all(),
    })

@login_required
def host(request, pk):
    """Host detail"""
    # TODO: Restrict to user's permissions
    print("** host ** pk: {}".format(pk))
    try:
        host = Host.objects.get(id=pk)
    except:
        host = None
        # return HttpResponseNotFound("404 - page not found.")

    try:
        agent = host.get_first_agent()
    except:
        agent = None
        agent_service = None
        
    # Retrieving data from a service
    # MVP currently supports only Wazuh
    # Wazuh record must already exist in database AgentService table
    # Name: Wazuh
    # Api_user: <api_user_name>
    # Api_pw: <api_pw>
    # TODO: AgentService should be set by Host - Agent relationship, yes?
    agent_service = AgentService.objects.filter(name='Wazuh').first()
    if agent_service:
        agent_service_api_address = "35.175.122.207:55000"
        agent_service_api_user = agent_service.api_user
        agent_service_api_pw = agent_service.api_pw
        
        import requests
        from requests.auth import HTTPBasicAuth
        r = requests.get('http://35.175.122.207:55000/sca/{}/?pretty'.format(agent.agent_id), auth=HTTPBasicAuth(agent_service_api_user, agent_service_api_pw))
        agent_service_data = r.json()
        agent_service_data_pretty = json.dumps(agent_service_data, sort_keys=True, indent=4)
        # Temporarily retreive checks information here
        checks_total = agent_service_data["data"]["items"][0]["total_checks"]
        checks_pass = agent_service_data["data"]["items"][0]["pass"]
        checks_pass_percent = round(checks_pass / checks_total * 100, 1)
        checks_fail = agent_service_data["data"]["items"][0]["fail"]
        checks_fail_percent = round(checks_fail / checks_total * 100, 1)

        #curl -u foo:bar -X GET  "http://35.175.122.207:55000/syscollector/006/packages?pretty"
        r_pkgs = requests.get('http://35.175.122.207:55000/syscollector/{}/packages?pretty'.format(agent.agent_id), auth=HTTPBasicAuth(agent_service_api_user, agent_service_api_pw))
        agent_service_data_pkgs = r_pkgs.json()
        agent_service_data_pkgs_pretty = json.dumps(agent_service_data_pkgs, sort_keys=True, indent=4)
        # pkgs_parsed = (json.loads(agent_service_data_pkgs))
        # print(agent_service_data_pkgs)

    else:
        agent_service_data_pretty = "Agent Service not defined or not supported."

    return render(request, "itsystems/host.html", {
        "host": host,
        "agent": agent,
        "agent_service_data": agent_service_data,
        "checks_total": checks_total,
        "checks_pass": checks_pass,
        "checks_fail": checks_fail,
        "checks_pass_percent": checks_pass_percent,
        "checks_fail_percent": checks_fail_percent,
        "agent_service_data_pkgs": agent_service_data_pkgs,
        "agent_service_data_pretty": agent_service_data_pretty,
        "agent_service_data_pkgs_pretty": agent_service_data_pkgs_pretty
    })

@login_required
def new_system(request):
    """Form to create new system instances"""
    # return HttpResponse("This is for new system instance.")
    if request.method == 'POST':
      form = SystemForm(request.POST)
      if form.is_valid():
        form.save()
        system = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('system_hosts_list', pk=system.pk)
    else:
        form = SystemForm()

    return render(request, 'itsystems/system_form.html', {
        'form': form,
        "system_form": SystemForm(request.user),
    })

@login_required
def new_host(request):
    """Form to create new system instances"""
    # return HttpResponse("This is for new host instance.")
    if request.method == 'POST':
      form = HostForm(request.POST)
      if form.is_valid():
        form.save()
        host = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('system_hosts_list', pk=host.system.pk)
    else:
        form = HostForm()

    return render(request, 'itsystems/host_form.html', {
        'form': form,
        "host_form": HostForm(request.user),
    })

@login_required
def new_agent(request):
    """Form to create new agent"""
    if request.method == 'POST':
      form = AgentForm(request.POST)
      if form.is_valid():
        form.save()
        agent = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('agents_list')
    else:
        form = AgentForm()

    return render(request, 'itsystems/agent_form.html', {
        'form': form,
        "agent_form": AgentForm(request.user),
    })

@login_required
def new_vendor(request):
    """Form to create new vendor"""
    if request.method == 'POST':
      form = VendorForm(request.POST)
      if form.is_valid():
        form.save()
        vendor = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('components_list')
    else:
        form = VendorForm()

    return render(request, 'itsystems/vendor_form.html', {
        'form': form,
        "vendor_form": VendorForm(request.user),
    })

@login_required
def new_agentservice(request):
    """Form to create new agent service"""
    if request.method == 'POST':
      form = AgentServiceForm(request.POST)
      if form.is_valid():
        form.save()
        agentservice = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('agents_list')
    else:
        form = AgentServiceForm()

    return render(request, 'itsystems/agentservice_form.html', {
        'form': form,
        "agentservice_form": AgentServiceForm(request.user),
    })

@login_required
def new_components(request):
    """Form to create new agent component"""
    # return HttpResponse("This is for a new component.")
    if request.method == 'POST':
      form = ComponentForm(request.POST)
      if form.is_valid():
        form.save()
        component = form.instance
        # system.assign_owner_permissions(request.user)
        return redirect('components_list')
    else:
        form = ComponentForm()

    return render(request, 'itsystems/component_form.html', {
        'form': form,
        "component_form": ComponentForm(request.user),
    })

