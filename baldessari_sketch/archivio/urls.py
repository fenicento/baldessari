from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

# import every app/autocomplete_light_registry.py


admin.autodiscover()


urlpatterns = patterns('',
    
    
    #index
	(r'^$|^index|baldessari_archivio', 'archivio.views.redirect_to_elenco_progetti'),
    # (r'^$|^index|baldessari_archivio', 'archivio.views.redirect_to_opere'),

    # "Opere" - projects and documents
    (r'opere/getInfo', 'archivio.views.getInfo'),
	(r'opere/documenti/getInfo', 'archivio.views.getInfo'),
	(r'opere/progetti/getInfo', 'archivio.views.getInfo'),
	# (r'^opere/$', 'archivio.views.redirect_to_elenco_progetti'),
    (r'^opere/$', 'archivio.views.opere'),	# TODO separare le view per progetti e documenti
    (r'^opere/documenti/$', 'archivio.views.documenti'),
    (r'^opere/documenti/galleria/$', 'archivio.views.galleria_doc'),
    (r'^opere/progetti/$', 'archivio.views.progetti'),
	(r'^opere/progetti/elenco/$', 'archivio.views.elenco_progetti'),
    (r'^opere/progetti/galleria/$', 'archivio.views.galleria_progetti'),
    (r'^opere/progetti/mappa/$', 'archivio.views.mappa_progetti'),	# TODO
    (r'^opere/progetti/timeline/$', 'archivio.views.timeline_progetti'),    # TODO
    (r'^opere/progetti/rete/$', 'archivio.views.rete_progetti'),    # TODO
    
    #persone
    (r'persone/$','archivio.views.rete_progetti'),
    
    #todo
    (r'^todo', 'archivio.views.working2'),
    
    #temi
    (r'^temi', 'archivio.views.elencoTemi'),
    (r'^biografia/$', 'archivio.views.biografia'),
    (r'^tema/(?P<themeid>\w+)', 'archivio.views.viewTheme'),
    
    # details
    (r'^opere/document/(?P<docsigle>\w+)', 'archivio.views.viewdoc'),
    (r'^opere/project/(?P<projsigle>\w+)', 'archivio.views.viewproj'),
    
    #JSON services
    (r'^service/progetti/$', 'archivio.views.filtraProgettiJson'),
    (r'^service/progetti/acprojname/$', 'archivio.views.acProjName'),
    (r'^service/progetti/acactorname/$', 'archivio.views.acActorName'),
    (r'^service/documenti/acdoc/$', 'archivio.views.acDoc'),
    (r'^service/rete/$', 'archivio.views.filtraReteJson'),
    (r'^service/documenti/$', 'archivio.views.documentiJson'),
    (r'^service/carteggi/$', 'archivio.views.carteggiJson'),
    
    # static views
    (r'^bibliografia/$', 'archivio.views.bibliografia2'),
    (r'^ricerca/$', 'archivio.views.ricerca'),
    (r'^museo_virtuale/$', 'archivio.views.museo_virtuale'),
    (r'^contatti/$', 'archivio.views.contatti'),
    (r'^login/$', 'archivio.views.login'),
    
)

# to show files stored in media folder
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))