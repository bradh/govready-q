from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import itsystems.views

urlpatterns = [
    url(r'^hello$', itsystems.views.index, name="hello"),
    url(r'^new$', itsystems.views.new_system),
    url(r'^hosts/new$', itsystems.views.new_host),
    url(r'^components/new$', itsystems.views.new_components),
    url(r'^components/list$', itsystems.views.components_list, name="components_list"),
    url(r'^hosts/list$', itsystems.views.host_list),
    url(r'^agents/list$', itsystems.views.agents_list, name="agents_list"),
    url(r'^(?P<pk>.*)/hosts', itsystems.views.system_hosts_list, name="system_hosts_list"),
    url(r'^agents/new$', itsystems.views.new_agent),
    url(r'^agentservice/new$', itsystems.views.new_agentservice),
    url(r'^hosts/(?P<pk>.*)', itsystems.views.host),
    url(r'', itsystems.views.system_list),

]
