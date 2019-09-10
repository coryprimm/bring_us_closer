from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^participant_landing$', views.participant_landing),
    url(r'^admin_landing$', views.admin_landing),
    url(r'^unformed_event/(?P<urlpassed_id>\d+)$', views.unformed_event),
    url(r'^formed_event/(?P<urlpassed_id>\d+)$', views.formed_event),
    url(r'^make_event/(?P<urlpassed_id>\d+)$', views.make_event),
    url(r'^join_event/(?P<urlpassed_id>\d+)$', views.join_event),
    url(r'^register$', views.register), #USED
    url(r'^logout$', views.logout),
    url(r'^admin_login$', views.admin_login), #USED
    url(r'^participant_login$', views.participant_login), #USED
    url(r'^delete/(?P<urlpassedevent_id>\d+)$', views.delete),
    url(r'^set_type/(?P<urlpassed_id>\d+)$', views.set_type),
    url(r'^finalize_event/(?P<urlpassed_id>\d+)$', views.finalize_event),
]

