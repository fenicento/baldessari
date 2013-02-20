from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    #index
	(r'^$|^index|baldessari_archivio', 'archivio.views.redirect_to_elenco_progetti'),
    # (r'^$|^index|baldessari_archivio', 'archivio.views.redirect_to_opere'),

    # "Biografia" == timeline
    (r'^biografia/$', 'archivio.views.biografia'),	# TODO

    # "Opere" - projects and documents
    (r'opere/getInfo', 'archivio.views.getInfo'),
	(r'opere/documenti/getInfo', 'archivio.views.getInfo'),
	(r'opere/progetti/getInfo', 'archivio.views.getInfo'),
	# (r'^opere/$', 'archivio.views.redirect_to_elenco_progetti'),
    (r'^opere/$', 'archivio.views.opere'),	# TODO separare le view per progetti e documenti
    (r'^opere/documenti/$', 'archivio.views.documenti'),
    (r'^opere/progetti/$', 'archivio.views.progetti'),
	(r'^opere/progetti/elenco/$', 'archivio.views.elenco_progetti'),
    (r'^opere/progetti/galleria/$', 'archivio.views.galleria_progetti'),
    (r'^opere/progetti/mappa/$', 'archivio.views.mappa_progetti'),	# TODO
    (r'^opere/progetti/timeline/$', 'archivio.views.timeline_progetti'),    # TODO

    # details
    (r'^opere/document/(?P<docsigle>\w+)', 'archivio.views.viewdoc'),
    (r'^opere/project/(?P<projsigle>\w+)', 'archivio.views.viewproj'),
    
    #JSON services
    (r'^service/progetti/$', 'archivio.views.filtraProgettiJson'),
    
    # static views
    (r'^bibliografia/$', 'archivio.views.bibliografia'),
    (r'^ricerca/$', 'archivio.views.ricerca'),
    (r'^museo_virtuale/$', 'archivio.views.museo_virtuale'),
    (r'^contatti/$', 'archivio.views.contatti'),
    (r'^login/$', 'archivio.views.login'),
    
    
    #admin functionalities
    (r'^savedatabase$', 'archivio.views.saveDataBase'),
    (r'^loaddatabase$', 'archivio.views.loadDataBase'),
    (r'^saveprojects$', 'archivio.views.saveProjects'),
    (r'^loadinitials$', 'archivio.views.loadInizziali'),
)

# to show files stored in media folder
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))