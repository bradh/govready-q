from django.contrib import admin

from .models import System, Host, AgentService, Agent, Vendor, Component


class HostsInLine(admin.TabularInline):
    model = Host

class AgentInLine(admin.TabularInline):
    model = Agent

class SystemAdmin(admin.ModelAdmin):
    ordering = ('name', 'sdlc_stage')
    list_display = ('name', 'sdlc_stage', 'id')
    inlines = [
        HostsInLine,
    ]

class HostAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'system', 'host_type', 'os', 'id')
    inlines = [
        AgentInLine,
    ]

class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'host', 'agent_service')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')

admin.site.register(System, SystemAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(AgentService)
admin.site.register(Agent, AgentAdmin)
