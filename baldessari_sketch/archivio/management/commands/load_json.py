from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def loadJson(self):
    reset(self)
    #call_command("update_from_json")
    loadProjects(self)
    loadDocuments(self)
    loadBiblio(self)
    loadActors(self)
    insertCarteggi(self)
    uploadImageInfo(self)

def reset(self):
    Project.objects.all().delete()
    Drawing.objects.all().delete()
    Publication.objects.all().delete()
    Actor.objects.all().delete()
    TimeInterval.objects.all().delete()
    Letter.objects.all().delete()
    print 'db reset' 
    
    

def loadProjects(self):
    # file = open(os.path.join(FILE_PATH, 'progetti.json'), 'r')
    file = open(os.path.join(FILE_PATH, 'progetti-correct.json'), 'r')
    projContent = StringIO(file.read())
    # projDict = json.load('[%s]' %  projContent[:-1])
    projDict = json.load(projContent)   #this dict will be updated with the content of docsDict
    file.close()
    
    for project in projDict:
        #get or create project
        try:
            p = Project.objects.get(denominazione = project['Denominazione'])

        except:
            p = Project(denominazione = project['Denominazione'])
            # p.tipo = project['tipo']
            p.tipo = project['tipo_1']
            p.tipo2 = project['tipo_2 (tipologia SAN)']
            p.address = project['indirizzo']
            # p.address = project['luogo']['indirizzo']
            # p.address = p.address
            
            try:
                p.latitude = float(project['latitude'])
                #p.latitude = project['luogo']['latitude']
                #p.latitude
                p.longitude = float(project['longitude'])
                #p.longitude = project['luogo']['longitude']
                #p.longitude
            except:
                p.latitude = None
                p.longitude = None
            p.sigla = project['sigla']
            p.save()
            
        # #persons
        # # coprogettista
        # try:
        #     actor = Actor.objects.get(name = project['coprogettista'])
        # except:	# actor not in the db
        #     if project['coprogettista'] is not None:
        #         actor = Actor(name = project['coprogettista'])
        #         actor = Actor(type = 'PE')
        #         actor.save()
        # 
        #         try:
        #             partic = Participation_set.get(project = project, actor = actor)
        #         except:
        #             partic = Participation(project = p, actor = actor, role = 'COP')
        #             partic.save()
        # 
        # # collaboratori
        # try:
        #     actor = Actor.objects.get(name = project['collaboratori'])
        # except:	# actor not in the db
        #     if project['collaboratori'] is not None:
        #         actor = Actor(name = project['collaboratori'])
        #         actor = Actor(type = 'PE')
        #         actor.save()
        # 
        #         try:
        #             partic = Participation_set.get(project = project, actor = actor)
        #         except:
        #             partic = Participation(project = p, actor = actor, role = 'COL')
        #             partic.save()
        # 
        # # committente
        # try:
        #     actor = Actor.objects.get(name = project['committente'])
        # except:	# actor not in the db
        #     if project['committente'] is not None:
        #         actor = Actor(name = project['committente'])
        #         actor = Actor(type = 'GR')
        #         actor.save()
        # 
        #         try:
        #             partic = Participation_set.get(project = project, actor = actor)
        #         except:
        #             partic = Participation(project = p, actor = actor, role = 'COM')
        #             partic.save()
        # 
        # # corrispondenti
        # try:
        #     actor = Actor.objects.get(name = project['corrispondenti'])
        # except:	# actor not in the db
        #     if project['corrispondenti'] is not None:
        #         actor = Actor(name = project['corrispondenti'])
        #         actor = Actor(type = 'N')
        #         actor.save()
        # 
        #         try:
        #             partic = Participation_set.get(project = project, actor = actor)
        #         except:
        #             partic = Participation(project = p, actor = actor, role = 'COR')
        #             partic.save()
        # 
        # # impresa / ditta
        # try:
        #     actor = Actor.objects.get(name = project['impresa/ditta'])
        # except:	# actor not in the db
        #     if project['impresa/ditta'] is not None:
        #         actor = Actor(name = project['impresa/ditta'])
        #         actor = Actor(type = 'GR')
        #         actor.save()
        # 
        #         try:
        #             partic = Participation_set.get(project = project, actor = actor)
        #         except:
        #             partic = Participation(project = p, actor = actor, role = 'COS')
        #             partic.save()



        # participations = project['partecipazioni']
        # for participation in participations:
           # #get or create actor
           # try:
               # actor = Actor.get(name = participation['attore'])
           # except:
               # actor = Actor(type = participation['tipo_del_attore'])
               # actor = Actor(name = participation['attore'])
               # actor.save()
           # #get or create participation
           # try:
               # partic = Participation_set.get(project = project, actor = actor)
           # except:
               # partic = Participation(project = p, actor = actor, role = participation['tipo_della_partecipazione'])
               # partic.save()
#                 
        # # bibliography
        # # bibliography = project['bibliografia']
        # bibliography = project['publications']
        # for bib in bibliography:
            # #get or create bibliography
            # try:
                # pub = Publication.get(name = bib['rough'])
            # except:
                # pub = Publication(name = bib['rough'])
                # pub.save()
            # #get or create link
            # try:
                # p.bibliografia.get(name = pub.name)
            # except:
                # p.bibliografia.add(pub)
                # p.save()
#         
        # dates
        dates = project['intervalli_di_tempo']
        for date in dates:
            #get or create timeinterval
            try:             
                begining = datetime.datetime.strptime(date['inizio'], "%Y")
                begYear = begining.year
            except:
                begining = datetime.datetime(1900,1,1,0,0) #TODO Soluzione temporanea, integrare i json con le date mancanti o ricostruire il db con date nullable
                begYear = begining.year
            
            try:    
                end = datetime.datetime.strptime(date['fine'], "%Y")
                endYear = end.year
            except:
                end = datetime.datetime(1900,1,1,0,0) #TODO Soluzione temporanea, integrare i json con le date mancanti o ricostruire il db con date nullable
                endYear = end.year
                
            try:
                d = TimeInterval.get(target = p, beginningDate = begining, endDate = end, beginningYear = begYear, endYear = endYear)
            except:
                d = TimeInterval(target = p, beginningDate = begining, endDate = end, beginningYear = begYear, endYear = endYear)
                d.save()
        
        # themes
        # themes = project['percorsi_tematici']
        # if themes:
            # for theme in themes:
                # # get or create Tematica
                # try:
                    # perc = Tematica.get(name = theme.name)
                # except:
                    # perc = Tematica(name = theme.name)
                    # perc.save()
    
    
def loadDocuments(self):
    print "ok"
    dateSeparator = '/'
    # file = open(os.path.join(FILE_PATH, 'disegni.json'), 'r')
    file = open(os.path.join(FILE_PATH, 'disegni-final.json'), 'r')
    docContent = StringIO(file.read())
    docDict = json.load(docContent) #this dict will be updated with the content of docsDict
    file.close()
    
    
    #get or create project
    for doc in docDict:
        try:
            d = Drawing.objects.get(segnatura = doc['segnatura'])
        except:
            d = Drawing(segnatura = doc['segnatura'])
            try:
                d.project = Project.objects.get(sigla = doc['sigla_progetto'])
                #debug lines!!!!!
                #projTime = TimeInterval.objects.filter(target = d.project)[0]
                #print d.project.sigla + str(projTime.beginningYear)
            except  Exception, e:
                print(e)
                continue
            
            # d.project = Project.objects.get(sigla = doc['sigla_progetto'])
            d.archivio = doc['sigla_archivio']
            # d.archivio = doc['sigla_archivio']
            
            try:
                data = doc['data']
                prec = doc['precisione']
    
                day = ''
                month = ''
                year = ''
                dateDay = 0
                dateMonth = 0
                dateYear = 0
    
                if data is not None:
                    nDateElements = data.count(dateSeparator)
                    if nDateElements + 1 == 3:   # 3 date elements - i.e. dd/mm/yyyy
                        day, sep, rest = data.partition(dateSeparator)
                        month, sep, year = rest.partition(dateSeparator)
    
                        if prec == 'year':
                            day = '1'
                            dateDay = None
                            month = '1'
                            dateMonth = None
                        elif prec == 'month':
                            day = '1'
                            dateDay = None
                            dateMonth = int(month)
                        else:
                            dateDay = int(day)
                            dateMonth = int(month)
    
                        dateYear = int(year)
                        d.data = datetime.datetime(int(year), int(month), int(day))
                        d.dataDay = dateDay
                        d.dataMonth = dateMonth
                        d.dataYear = dateYear
                else:
                    #print 'finding date intervals of project '+d.project.sigla
                    #print d.project 
                    projTime = TimeInterval.objects.filter(target = d.project)[0]
                    #print projTime
                    #print str(projTime.beginningYear)
                    if projTime.beginningYear != None:
                        d.dateYear = projTime.beginningYear
                        d.data = datetime.datetime(int(d.dateYear), 1, 1)
                    else:    
                        d.data = None
                        d.dateDay = None
                        d.dateMonth = None
                        d.dateYear = None
            except Exception, e:
                # print e
                print e
                
                d.data = None
                d.dateDay = None
                d.dateMonth = None
                d.dateYear = None
            
            # d.formato = doc['formato']
            d.largezza = doc['larghezza']
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

def loadBiblio(self):
    filebib = open(os.path.join(FILE_PATH, 'biblio.json'), 'r')
    bibContent = StringIO(filebib.read())
    bibDict = json.load(bibContent) #this dict will be updated with the content of docsDict
    filebib.close()
    
    Publication.objects.all().delete()
    
    i = 0
    
    for pub in bibDict:     # for each publication
        i = i+1
        try:
            p = Publication.objects.get(name = pub['Titolo'])
        except:
            pubProj = pub['Sigla']
            #print pubProj
            pubString = pub['Titolo']
            
            if pubString == None:
                pubString = 'blank'
            
            pubPages = pub['Pagina']
            if pubPages == None:
                pubPages = 'blank' 
                
            pubFigs = pub['Figura']
            if pubFigs != None:
                if pubPages != 'blank':
                    pubPages = pubPages + " " + pubFigs
                else: 
                    pubPages = pubFigs
            
            pubType = pub['Tipo']
            if pubType == None:
                pubType = 'blank' 
            
            # try:
                # pubString = pub['Bibliografia']
            # except:
            newPub = Publication(name = pubString, pages = pubPages, sup_infos = pubType)
            newPub.save()
            try:
                proj = Project.objects.get(sigla = pubProj)
                proj.bibliografia.add(newPub)
                proj.save()
            except Exception, e:
                print e
                #print pubProj

def loadActors(self):
    fileact = open(os.path.join(FILE_PATH, 'attori-final.json'), 'r')
    actContent = StringIO(fileact.read())
    actDict = json.load(actContent) #this dict will be updated with the content of docsDict
    fileact.close()
    
    Actor.objects.all().delete()
    
    i = 0
    
    for act in actDict:     # for each publication
        i = i+1
        try:
            p = Project.objects.get(sigla = act['SIGLA'])
        except:
            #print "no project found with ID "+ act['SIGLA']
            continue
            
        try:
            a = Actor.objects.get(name = act['NOMI'])
            newPar= Participation(actor = a, project = p, role = act["TIPO"])
        except:
            actName = act['NOMI']
            newAct= Actor(name = actName, id = i)
            newPar= Participation(actor = newAct, project = p, role = act["TIPO"])
            newAct.save()
        try:    
            newPar.save()
        except:
            print "could not save participation"
            continue  
    print Participation.objects.all()
    
    
    
    
def uploadImageInfo(self):
    call_command("attribute_images")
    #call_command("attribute_letters")
    
    
def insertCarteggi(self):
    
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    DRAWS_PATH = os.path.join(FILE_PATH, '/Users/davide/Documents/Baldessari/source/progetto_django-nuovi_models/baldessari_sketch/media/img_documents/carteggi/')
    
    #load values
    projects=Project.objects.all()
    letters=Letter.objects.all()
    times=TimeInterval.objects.all()
    
    #loop on all projects
    for p in projects:
        
        #check if a folder exists for the project
        currPath=DRAWS_PATH+p.sigla.lower()
        if os.path.isdir(currPath):
            
            #take all files in the folder
            for cart in os.listdir(currPath):
                
                #retrieve signature from filename
                sign=os.path.splitext(cart)[0]
                
                
                
                #check if letter is already stored
                try:
                    newLetter = letters.get(segnatura = sign)
                
                #if letter is new, add it
                except:
                    newLetter = Letter(segnatura=sign, project=p)
                    
                    #assign the first beginning year of the project to the letter
                    for t in times:
                        if t.target == p:
                            newLetter.dataYear=t.beginningYear
                            break
                            
                    #store the new letter
                    newLetter.save()
                    
                    
                    
                    
                    
def writeProjectsJson(self): 
    jsonProj=[]
    projects=Project.objects.all()
    for p in projects:
        if p.latitude!=None and p.longitude!=None:
            jsonProj.append(dict(p))
    s = json.dumps(jsonProj)

    f = open('projectsMap.json', 'a')
    f.write(s + "\n")
    f.close()
        
    
    
    
class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        loadJson(self)