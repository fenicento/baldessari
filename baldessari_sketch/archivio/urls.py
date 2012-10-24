from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    #index
    (r'^$|^index|baldessari_archivio', 'archivio.views.redirect_to_opere'),
    (r'^biografia/$', 'archivio.views.biografia'),
    #(r'^opere', 'archivio.views.opere'),
    (r'^opere/document/(?P<docsigle>\w+)', 'archivio.views.viewdoc'),
    (r'^opere/project/(?P<projsigle>\w+)', 'archivio.views.viewproj'),
    (r'opere/getInfo', 'archivio.views.getInfo'),
    (r'^opere/', 'archivio.views.opere'),
    
    (r'^bibliografia/$', 'archivio.views.bibliografia'),
    (r'^ricerca/$', 'archivio.views.ricerca'),
    (r'^museo_virtuale/$', 'archivio.views.museo_virtuale'),
    (r'^contatti/$', 'archivio.views.contatti'),
    (r'^login/$', 'archivio.views.login'),
    
    
    #admin functionnalities
    (r'^savedatabase$', 'archivio.views.saveDataBase'),
    (r'^loaddatabase$', 'archivio.views.loadDataBase'),
    (r'^loadinitials$', 'archivio.views.loadInizziali'),
)