
from archivio.models import *
from django.contrib import admin
from django import forms


class BioModelForm( forms.ModelForm ):
    testo = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = BioDetail


#--------------------- MAKING PROJECT INTERFACE --------------------------------------------#
class TimeIntervalInLine(admin.TabularInline):
    model = TimeInterval
    extra = 1

class BiblioInLine(admin.TabularInline):
    model = Project.bibliografia.through
    raw_id_fields = ('publication',)
    extra = 1

class DesigniInLine(admin.TabularInline):
    #raw_id_fields = ("segnatura",)
    model = Drawing
    extra = 1
    
class CarteggiInLine(admin.TabularInline):
    #raw_id_fields = ("segnatura",)
    model = Letter
    extra = 1

class ParticipationInLine(admin.TabularInline):
    model = Participation
    raw_id_fields = ('actor',)
    extra = 1

# class PercorsiInLine(admin.TabularInline):
    # model = Project.percorsi_tematici.through
    # extra = 3
    
class ProjAdmin(admin.ModelAdmin):
    
    #fields = ['denominazione', 'tipo', 'tipo2','descrizione_prog','address','latitude', 'longitude', 'sigla']
    #to add: persone et participation
    list_display = ('denominazione', 'sigla', 'tipo', 'tipo2')
    search_fields = ('denominazione', 'sigla',)
    filter_horizontal=('persone','bibliografia',)
    
    inlines = [TimeIntervalInLine, ParticipationInLine, BiblioInLine]


#--------------------- MAKING DRAWINGS INTERFACE --------------------------------------------#

'''
class DesigniFilesInLine(admin.TabularInline):
    model = DrawingFile
    extra = 3
'''
    
class DisegnoAdmin(admin.ModelAdmin):
    raw_id_fields = ('project',)
    date_hierarchy = ('data')
    search_fields = ('segnatura',)
    list_display = ('segnatura', 'data', 'archivio')
    #filter_horizontal=('project',)
    #inlines = [DesigniFilesInLine]
    
    
    
class CarteggiAdmin(admin.ModelAdmin):
    raw_id_fields = ('project',)
    date_hierarchy = ('data')
    search_fields = ('segnatura',)
    list_display = ('segnatura',)
    #filter_horizontal=('project',)

#--------------------- MAKING ACTORS INTERFACE --------------------------------------------#

class ProjettoInLine(admin.TabularInline):
    model = Participation
    raw_id_fields = ('project',)
    extra = 1

class ActorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'type','id',)
    inlines = [ProjettoInLine]

#--------------------- MAKING REFERENCE INTERFACE --------------------------------------------#
class RefInLine(admin.TabularInline):
    model = Project.bibliografia.through
    raw_id_fields = ('project',)
    extra = 1

class RefAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'provenance')
    inlines = [RefInLine]
    
#--------------------- MAKING BIOGRAPHY INTERFACE --------------------------------------------#    

class BioAdmin(admin.ModelAdmin):
    model=BioDetail
    form = BioModelForm
    list_display = ('id','titolo','testo','immagine','didascalia','startDate','endDate',)
    list_editable = ('titolo','testo','immagine','didascalia','startDate','endDate',)
    list_display_links=('id',)
    #list_display = ('titolo', 'startDate','endDate')
    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', BioModelForm)
        return super(BioAdmin, self).get_changelist_form(request, **kwargs)


class ThemeInLine(admin.TabularInline):
    model = ThemeDetail
    exclude = ('imgUrl',)
    extra = 1

class ThemeAdmin(admin.ModelAdmin):
    model=Tematica
    list_display = ('name',)
    inlines = [ThemeInLine]
    
    

admin.site.register(Project, ProjAdmin)
admin.site.register(Drawing, DisegnoAdmin)
admin.site.register(Letter, CarteggiAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Publication, RefAdmin)
admin.site.register(BioDetail, BioAdmin)
admin.site.register(Tematica, ThemeAdmin)
# admin.site.register(Tematica, PercorsiAdmin)