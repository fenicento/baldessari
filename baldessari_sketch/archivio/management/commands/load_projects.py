from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"

file = open(os.path.join(FILE_PATH, 'progetti-correct.json'), 'r')
projContent = StringIO(file.read())
# projDict = json.load('[%s]' %  projContent[:-1])
projDict = json.load(projContent)   #this dict will be updated with the content of docsDict
file.close()

# date variables

for project in projDict:

    try:
        p = Project.objects.get(sigla = project['sigla'])
        p.materiali = project['materiali']
        p.save()
        print ("progetto esistente: " + project['sigla'])

    except:     # project does not exist
        print "progetto non esistente"
    
    

       