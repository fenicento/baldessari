
from archivio.models import *
from django.contrib import admin



#--------------------- MAKING PROJECT INTERFACE --------------------------------------------#
class TimeIntervalInLine(admin.TabularInline):
    model = TimeInterval
    extra = 1

class BiblioInLine(admin.TabularInline):
    model = Project.bibliografia.through
    extra = 1

class DesigniInLine(admin.TabularInline):
    model = Drawing
    extra = 1

class ParticipationInLine(admin.TabularInline):
    model = Participation
    extra = 1

# class PercorsiInLine(admin.TabularInline):
    # model = Project.percorsi_tematici.through
    # extra = 3
    
class ProjAdmin(admin.ModelAdmin):
    
    fields = ['denominazione', 'tipo', 'tipo2', 'address','latitude', 'longitude', 'sigla']
    #to add: persone et participation
    list_display = ('denominazione', 'sigla', 'tipo', 'tipo2')
    search_field = ('denominazione', 'tipo', 'address', 'tipo2')
    inlines = [TimeIntervalInLine, ParticipationInLine, DesigniInLine, BiblioInLine]


#--------------------- MAKING DRAWINGS INTERFACE --------------------------------------------#

'''
class DesigniFilesInLine(admin.TabularInline):
    model = DrawingFile
    extra = 3
'''
    
class DisegnoAdmin(admin.ModelAdmin):
    date_hierarchy = ('data')
    search_field = ('segnatura', 'tecnica', 'strumento')
    list_display = ('segnatura', 'data', 'archivio')
    #inlines = [DesigniFilesInLine]

#--------------------- MAKING ACTORS INTERFACE --------------------------------------------#

class ProjettoInLine(admin.TabularInline):
    model = Project.persone.through
    extra = 2

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    inlines = [ProjettoInLine]

#--------------------- MAKING REFERENCE INTERFACE --------------------------------------------#
class RefInLine(admin.TabularInline):
    model = Project.bibliografia.through
    extra = 1

class RefAdmin(admin.ModelAdmin):
    list_display = ('name', 'provenance')
    inlines = [RefInLine]

admin.site.register(Project, ProjAdmin)
admin.site.register(Drawing, DisegnoAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Publication, RefAdmin)
# admin.site.register(Tematica, PercorsiAdmin)