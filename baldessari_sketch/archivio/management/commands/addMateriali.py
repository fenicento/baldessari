from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
from StringIO import StringIO
import re
import os

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"

def addMateriali(self):

    file = open(os.path.join(FILE_PATH, 'progetti-correct.json'), 'r')
    projContent = StringIO(file.read())
    projDict = json.load(projContent)   #this dict will be updated with the content of docsDict
    file.close()
    
    # date variables
    
    for project in projDict:
        print project['sigla']
        try:
            p = Project.objects.get(sigla = project['sigla'])
            p.materiali = project['materiali_raw']
            p.save()
            print ("progetto esistente: " + project['sigla'])
    
        except:     # project does not exist
            print "progetto non esistente"
        
    

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        addMateriali(self)