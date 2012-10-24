from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
from StringIO import StringIO
from django.core.files import File
import os.path
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#global nbreOfProjects = 0
#global nbreOfDocs = 0


def defActor(role, self, proj, p):
            nome = proj[role]
            if(len(nome) > 2):
                try:
                    match = Actor.objects.get(name=nome)
                except:
                    match = Actor(name=nome)
                    match.save()
                    
                #m2m relations
                ROLE_CHOICE = {
                       'coprogettista/i':'COP',
                       'collaboratore/i':'COL',
                       'committente':'COM',
                       'costruttore':'COS',
                       }
                    
                r = Participation.objects.create(actor = Actor.objects.get(name=nome),
                                                project = Project.objects.get(denominazione = proj["denominazione"]),
                                                role = ROLE_CHOICE[role]
                                  )
                r.save()
                #self.stdout.write('Successfully created actor '+match.name+'\n') 




def parseProjects(projectJson, self):
        #open the project
        projF = open(projectJson, "r")
        projContent = StringIO(projF.read())
        projDict = json.load(projContent)#this dict will be updated with the content of docsDict
        
        global nbrProjects
        nbrProjects += len(projDict)
        
        
        #parse the dictionnary to create entries in the database
        for proj in projDict:

                    p = Project(sigla = proj["sigla"])
                    p.denominazione = proj["denominazione"]
                    p.tipo = proj["tipo"]
                    p.save()
 
                    try:
                        p.address = proj["luogo"]["raw"]
                        coords = proj["luogo"]["coordinate"]
                        p.latitude = float(coords[0])
                        p.longitude = float(coords[1])
                    except:
                        self.stdout.write('Problem of location with project '+p.denominazione+'\n')
                    
                    #to-do : date formatting
                    date = proj["data"]#retrieve the field data
                    datedec = re.split('[;-]', date)#split in case of multiple time intervalls
                    for stri in datedec:#clean the strings
                        stri.strip()
                    
                    for text in datedec:  
                        date_data  = text.split("/")#split the dates of begining and end
                        intervall = TimeInterval()#create the intervall
                        if(len(date_data) == 2):
                                intervall.begining = datetime.datetime(int(date_data[0]), 1, 1, 0, 0)
                                intervall.end = datetime.datetime(int(date_data[1])+1900, 1, 1, 0, 0)   
                        else:
                                intervall.begining = datetime.datetime(int(text), 1, 1, 0, 0)
                                intervall.end = datetime.datetime(int(text[2:3])+1900, 1, 1, 0, 0)
                        intervall.target = Project.objects.get(denominazione = proj["denominazione"])
                        intervall.save()#save the intervall
                    
                    p.sigla = proj["sigla"]
                    
                    #fill bibliography
                    try:
                        bibliography = proj['bibliografia']
                        for citation in bibliography:
                            if(len(citation) > 2):
                                try:
                                    match = Publication.objects.get(name=citation)
                                except:
                                    match = Publication(name=citation)
                                    #self.stdout.write('Successfully created quotation '+citation+'\n')               
                                match.save()
                                #todo: add the M2M relation 
                                p.bibliografia.add(Publication.objects.get(name=citation))
                    except:
                        self.stdout.write('No bibliography added for project '+p.denominazione+'\n')    
                    #fill actors
                    defActor('committente', self, proj, p)
                    defActor('collaboratore/i', self, proj, p)
                    defActor('coprogettista/i', self, proj, p)
                    if "costruttore" in proj:
                            defActor('costruttore', self, proj, p)
                    p.save()

def linkImages(self):
    staticpath = os.path.join(FILE_PATH, '../../../static/img_documents')
    for doc in os.listdir(staticpath):#parse projects
        docdb = Drawing.objects.get(segnatura = doc)
        localpath = os.path.join(FILE_PATH, '../../../static/img_documents/'+doc+'/')
        rank = 1
        for file in os.listdir(localpath):
            f = open(localpath+file, 'r')
            print f
            filou = DrawingFile.objects.create(
                                image = File(open(localpath+file, 'r')),
                                rank = rank,
                                parent = docdb
                                )
            filou.save()
            rank= rank + 1





def parseDocuments(newDocFile, self):
        docF = open(newDocFile, "r")
        docC = StringIO(docF.read())
        docDict = json.load(docC)#this dict will be updated with the content of docsDict
        docF.close()
        
        global nbrDocs
        nbrDocs += len(docDict)
                
        
        for doc in docDict:
            if str(doc['segnatura']) != 'segnatura ':
                    d = Drawing(segnatura = doc["segnatura"])
                    d.archivio = 'ALB'
                    projectTag = ''
                    
                    nameRough = doc['segnatura'].split('_')
                    projectTag = nameRough[1]
                    
                    
                    try:
                        if projectTag == 'PB1' or projectTag == 'PB2' or projectTag == 'PB3' or projectTag == 'PB4' or projectTag == 'PB5' or projectTag == 'PB6' or projectTag == 'PB7' or projectTag == 'PB8' or projectTag == 'PB9':
                            projectTag = 'PBM'
                        
                        if projectTag == 'AT4':
                            projectTag = 'ADG'
                        d.project = Project.objects.get(sigla = projectTag)
                    except:
                        parts = doc['segnatura'].split('_')
                        projectTag = parts[1]
                        print "problem with document " + d.segnatura + " from "+projectTag
                        
                    if(doc['data'] and doc['data'] != 'null' and doc['data'] != 'data'):
                        #there are two formats of dates in the data : "00/00/1937", and "Sat Feb 18 00:00:00 CET 1933"
                        #first type (we match a / to check it):
                        stringdate = str(doc['data'])
                        
                        if ", " in str(doc['data']):
                            dates = doc['data'].split(', ')
                            stringdate = dates[0]
                        
                        if "/" in stringdate :
                            raws = stringdate.split('/')
                            if(raws[0] == '00'):
                                day = 1
                            else:
                                day = int(raws[0])
                            if(raws[1] == '00'):
                                month = 1
                            else:
                                month = int(raws[1])
                            year = int(raws[2])
                            d.data = datetime.datetime(year, month, day, 0, 0, 0, 0)
                        #second type of date format
                        else:
                            Months = {                  #<---- this dictionnary transform the notation of months into an int
                                      "Jan" : 1,
                                      "Feb" : 2,
                                      "Mar" : 3,
                                      "Apr" : 4,
                                      "May" : 5,
                                      "Jun" : 6,
                                      "Jul" : 7,
                                      "Aug" : 8,
                                      "Sep" : 9,
                                      "Oct" : 10,
                                      "Nov" : 11,
                                      "Dec" : 12
                                      }
                            raws = doc["data"].split(' ')
                            
                            year = int(raws[5])
                            month = Months[raws[1]]  
                            day = int(raws[2])
                            d.data = datetime.datetime(year, month, day, 0, 0, 0, 0)        
         
                            d.prestiti=False
                            
                    #get width and height of drawing(formatto)
                    if(doc['formato'] and doc['formato'] != 'null' and doc['formato'] != 'formato'):
                        try:
                            vals = doc['formato'].split('x')
                            for val in vals : val.strip()
                            #get width of drawing
                            decompw = vals[0].split(',')
                            if(len(decompw)==2): d.largezza = float('.'.join(decompw))
                            else : d.largezza = int(decompw[0])
                            
                            #get height of drawing
                            decomph = vals[1].split(',')
                            if(len(decomph)==2): d.altezza = float('.'.join(decomph))
                            else : d.altezza = int(decomph[0])
                        except :
                            d.largezza = None
                            d.altezza = None
                    
                    
                    if(doc['collocazione'] != 'null' ): d.collocazione = doc['collocazione']
                    if(doc['riproduzione'] != 'null' ): d.riproduzione = doc['riproduzione']
                    if(doc['tecnica'] != 'null' ): d.tecnica = doc['tecnica']
                    if(doc['tipo'] != 'null' ): d.tipo = doc['tipo']
                    if(doc['scala'] != 'null' ): d.scala = doc['scala']
                    if(doc['strumento'] != 'null' ): d.strumento = doc['strumento']
                    if(doc['supporto'] != 'null' ): d.supporto = doc['supporto']
                    if(doc['cartigli'] != 'null' ): d.cartigli = doc['cartigli']
                    if(doc['annotazioni'] != 'null' ): d.annotazioni = doc['annotazioni']
                    if(doc['multipli'] != 'null' ): d.collocazione = doc['collocazione']
                    if(doc['formato_cornice'] != 'null' ): d.formato_cornice = doc['formato_cornice']
                    if(doc['conservazione'] != 'null' ): d.conservazione = doc['conservazione']
                    if(doc['restauri'] != 'null' ): d.restauri = doc['restauri']
                    d.sigla_archivio = "ALB"
                        
                    d.save()
        


class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
            global nbrProjects
            global nbrDocs
            nbrProjects = 0
            nbrDocs = 0
            parseProjects(os.path.join(FILE_PATH, 'projects.json'), self)
            parseDocuments(os.path.join(FILE_PATH, 'documents-3.json'), self)
            
            nbrProjDatabase = len(Project.objects.all())
            nbrDocDatabase = len(Drawing.objects.all())
            
            print "there should be " + str(nbrProjects)+" projects, there are "+str(nbrProjDatabase)
            print "there should be " + str(nbrDocs)+" documents, there are "+str(nbrDocDatabase)