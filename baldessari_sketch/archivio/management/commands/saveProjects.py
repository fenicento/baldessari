from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path


def saveAll(self):
    saveProjects(self)
    saveDrawings(self)
    saveLetters(self)
    saveDates(self)
                    
def saveProjects(self): 
    jsonProj=[]
    projects=Project.objects.all().values()
   
    for p in projects:
        if p['latitude']!=None and p['longitude']!=None:
            
            jsonProj.append(p)
    s = json.dumps(jsonProj)

    f = open('projectsExp.json', 'a')
    f.write(s + "\n")
    f.close()
    
def saveDrawings(self): 
    jsonProj=[]
    docs=Drawing.objects.all().values()

    for d in docs:
        if d['data']!=None:
            
            del d['data']
            jsonProj.append(d)
    print jsonProj
    s = json.dumps(jsonProj)

    f = open('drawingsExp.json', 'a')
    f.write(s + "\n")
    f.close()
    
def saveDates(self): 
    jsonProj=[]
    docs=TimeInterval.objects.all().values()

    for d in docs:
        if d['beginningDate']!=None and d['endDate']!=None:
            
            del d['beginningDate']
            del d['endDate']
            jsonProj.append(d)
    print jsonProj
    s = json.dumps(jsonProj)

    f = open('DatesExp.json', 'a')
    f.write(s + "\n")
    f.close()
        
        
def saveLetters(self): 
    jsonProj=[]
    docs=Letter.objects.all().values()
    
    for d in docs:
        if d['dataYear']!=None:
            
            
            jsonProj.append(d)
    print jsonProj 
    s = json.dumps(jsonProj)

    f = open('lettersExp.json', 'a')
    f.write(s + "\n")
    f.close()
    
                
        
class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        saveAll(self)   

    