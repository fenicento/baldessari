from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, os.path, re
from StringIO import StringIO
from django.core.files import File
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def saveJson(self):
    saveProjects(self)
    saveDocuments(self)

def saveProjects(self):
    file = open(os.path.join(FILE_PATH, 'projects.json'), 'w')
    projects = []
    Projects = Project.objects.all()
    for project in Projects:
        pjson = {}
        pjson['denominazione'] = project.denominazione
        pjson['tipo'] = project.tipo
        pjson['tipo2'] = project.tipo2
        pjson['luogo'] = {}
        luogo = pjson['luogo']
        luogo['indirizzo'] = project.address
        luogo['latitude'] = project.latitude
        luogo['longitude'] = project.longitude
        
        pjson['sigla'] = project.sigla
        
        #persone        
        pjson['partecipazioni'] = []
        partecipazioni = project.participation_set.filter(project= project)
        for partecipazione in partecipazioni:
            part = {}
            part['attore'] = partecipazione.actor.name
            part['tipo_del_attore'] = partecipazione.actor.type
            part['tipo_della_partecipazione'] = partecipazione.role
            pjson['partecipazioni'].append(part)
            
        #bibliografia
        pjson['publications'] = []
        pub = project.bibliografia.all()
        for publication in pub:
            p = {}
            p['rough'] = publication.name
            pjson['publications'].append(p)
        
        #times
        pjson['intervalli_di_tempo'] = []
        intervalli = TimeInterval.objects.filter(target = project)
        for intervallo in intervalli:
            interv = {}
            interv['inizzio'] = intervallo.begining.year
            interv['fine'] = intervallo.end.year
            pjson['intervalli_di_tempo'].append(interv)

        # percorsi tematici
        pjson['percorsi_tematici'] = []
        percorsi = project.percorsi_tematici.all()
        for perc in percorsi:
            percorso = {}
            percorso['nome'] = percorso.name
            pjson['percorsi_tematici'].append(perc)
            
        projects.append(pjson)
        
    file.write(json.dumps(projects))
    file.close()
    
    
def saveDocuments(self):
    file = open(os.path.join(FILE_PATH, 'documents.json'), 'w')
    drawings = []
    Drawings = Drawing.objects.all()
    for drawing in Drawings:
        djson = {}
        #project
        djson['progetto'] = drawing.project.sigla
        #archivio
        djson['archivio'] = drawing.archivio
        #data
        try:
            djson['data'] = drawing.data.year
        except:
            djson['data'] = ''
        
        djson['prestiti'] = drawing.prestiti
        djson['largezza'] = drawing.largezza
        djson['altezza'] = drawing.altezza
        djson['annotazioni'] = drawing.annotazioni
        djson['tecnica'] = drawing.tecnica
        djson['supporto'] = drawing.supporto
        djson['tipo'] = drawing.tipo
        djson['segnatura'] = drawing.segnatura
        djson['strumento'] = drawing.strumento
        djson['scala'] = drawing.scala
        djson['sigla_archivio'] = drawing.sigla_archivio
        djson['multipli'] = drawing.multipli
        djson['restauri'] = drawing.restauri
        djson['formato_cornice'] = drawing.formato_cornice
        djson['collocazione'] = drawing.collocazione
        djson['conservazione'] = drawing.conservazione
        djson['riproduzione'] = drawing.riproduzione
        djson['cartigli'] = drawing.cartigli     
        
        drawings.append(djson)
        
    file.write(json.dumps(drawings))
    file.close()

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        saveJson(self)
        #try:
            #parseJson(os.path.join(FILE_PATH, 'baldessari.json'), self)
            #linkImages(self)
        #except:
           # try:
            #    parseJson(args[0], self)
           # except:
             ##   self.stdout.write("\nDEVI SCRIVERE UN INDIRIZZO DI FILE JSON, DAI!\n\n\
              #  esempio : python manage.py update_from_json \"C:\/baldessari.json\"\
             #   \n")