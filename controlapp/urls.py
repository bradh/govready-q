from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import controlapp.views

urlpatterns = [
    url(r'^hello$', controlapp.views.index, name="hello"),
    # url(r'^new$', itsystems.views.new_system),
    # url(r'^hosts/new$', itsystems.views.new_host),

]
