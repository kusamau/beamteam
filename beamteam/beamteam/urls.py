from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url


# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",                        
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    #("^admin/", include(admin.site.urls)),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.
)


urlpatterns += patterns('beamteam.views.process',
    (r'^beam$', 'process_beam'),
)

urlpatterns += patterns('beamteam.views.data',
    (r'^data$', 'process'),
)
