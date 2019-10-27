from django import forms
from django.forms import ModelForm

from itsystems.models import System
from itsystems.models import Host
from itsystems.models import Agent
from itsystems.models import Component
from itsystems.models import Vendor

class SystemForm(ModelForm):

    class Meta:
        model = System
        fields = ['name', 'sdlc_stage']
        labels = {
            'name': ('Name'),
            'sdlc_stage': ('Software Development Life Cycle (SDLC) Stage'),
        }

class HostForm(ModelForm):

    class Meta:
        model = Host
        fields = ['name', 'host_type', 'os', 'system']
        labels = {
            'name': ('Name'),
            'host_type': ('Host Type'),
            'os': ('Operating System'),
            'system': ('System Instance'),
        }

class AgentForm(ModelForm):

    class Meta:
        model = Agent
        fields = ['agent_id', 'agent_service', 'host',]
        labels = {
            'agent_id': ('Agent Id'),
            'agent_service': ('Agent Service'),
            'host': ('Host Instance'),
        }

class VendorForm(ModelForm):

    class Meta:
        model = Vendor
        fields = ['name',]
        labels = {
            'name': ('Name'),
        }

class ComponentForm(ModelForm):

    class Meta:
        model = Component
        fields = ['name', 'vendor', 'version',]
        labels = {
            'name': ('Name'),
            'vendor': ('Vendor'),
            'version': ('Version'),
        }