from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
from StringIO import StringIO
from django.core.files import File
import os.path
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def loadJson(self):
    reset(self)
    #call_command("update_from_json")
    loadProjects(self)
    loadDocuments(self)

def reset(self):
    Project.objects.all().delete()
    Drawing.objects.all().delete()
    Publication.objects.all().delete()
    Actor.objects.all().delete()
    TimeInterval.objects.all().delete()
    DrawingFile.objects.all().delete()
    
    

def loadProjects(self):
    file = open(os.path.join(FILE_PATH, 'projects.json'), 'r')
    projContent = StringIO(file.read())
    projDict = json.load(projContent)#this dict will be updated with the content of docsDict
    file.close()
    
    for project in projDict:
        #get or create project
        try:
            p = Project.objects.get(denominazione = project['denominazione'])
        except:
            p = Project(denominazione = project['denominazione'])
            p.tipo = project['tipo']
            p.tipologia = project['tipologia']
            p.address = project['luogo']['indirizzo']
            
            try:
                p.latitude = project['luogo']['latitude']
                p.longitude = project['luogo']['longitude']
            except:
                p.latitude = None
                p.longitude = None
            p.sigla = project['sigla']
            p.save()
            
        #persons
        participations = project['partecipazioni']
        for participation in participations:
            #get or create actor
            try:
                actor = Actor.get(name = participation['attore'])
            except:
                actor = Actor(type = participation['tipo_del_attore'])
                actor = Actor(name = participation['attore'])
                actor.save()
            #get or create participation
            try:
                partic = Participation_set.get(project = project, actor = act)
            except:
                partic = Participation(project = p, actor = actor, role = participation['tipo_della_partecipazione'])
                partic.save()
                
        #bibliography
        bibliography = project['publications']
        for bib in bibliography:
            #get or create bibliography
            try:
                pub = Publication.get(name = bib['rough'])
            except:
                pub = Publication(name = bib['rough'])
                pub.save()
            #get or create link
            try:
                p.bibliografia.get(name = pub.name)
            except:
                p.bibliografia.add(pub)
                p.save()
        
        #dates
        dates = project['intervalli_di_tempo']
        for date in dates:
            #get or create timeinterval
                        
            begining = datetime.datetime(date['inizzio'], 1, 1, 0, 0, 0, 0)
            end = datetime.datetime(date['fine'], 1, 1, 0, 0, 0, 0)
            
            try:
                d = TimeInterval.get(target = p, begining = begining, end = end)
            except:
                d = TimeInterval(target = p, begining = begining, end = end)
                d.save()
        

    
    
def loadDocuments(self):
    print "ok"
    file = open(os.path.join(FILE_PATH, 'documents.json'), 'r')
    docContent = StringIO(file.read())
    docDict = json.load(docContent)#this dict will be updated with the content of docsDict
    file.close()
    
    
    #get or create project
    for doc in docDict:
        try:
            d = Drawing.objects.get(segnatura = doc['segnatura'])
        except:
            d = Drawing(segnatura = doc['segnatura'])
            d.project = Project.objects.get(sigla = doc['progetto'])
            d.archivio = doc['archivio']
            
            try:
                date = datetime.datetime(doc['data'], 1, 1, 0, 0, 0, 0)
                d.data = date
            except:
                d.data = None
            
            d.prestiti = doc['prestiti']
            d.largezza = doc['largezza']
            d.altezza = doc['altezza']
            d.annotazioni = doc['annotazioni']
            d.tecnica = doc['tecnica']
            d.supporto = doc['supporto']
            d.tipo = doc['tipo']
            d.segnatura = doc['segnatura']
            d.strumento = doc['strumento']
            d.scala = doc['scala']
            d.sigla_archivio = doc['sigla_archivio']
            d.multipli = doc['multipli']
            d.restauri = doc['restauri']
            d.formato_cornice = doc['formato_cornice']
            d.collocazione = doc['collocazione']
            d.conservazione = doc['conservazione']
            d.riproduzione = doc['riproduzione']
            d.cartigli = doc['cartigli']
               
            d.save()
            
            
            
class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        loadJson(self)