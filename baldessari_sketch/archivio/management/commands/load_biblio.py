from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"

file = open(os.path.join(FILE_PATH, 'bibliografia.json'), 'r')
bibContent = StringIO(file.read())
bibDict = json.load(bibContent) #this dict will be updated with the content of docsDict
file.close()

Publication.objects.all().delete()

i = 0

for pub in bibDict:     # for each publication
    i = i+1
    try:
        p = Publication.objects.get(name = pub['Bibliografia'])
    except:
        pubProj = pub['Sigla']
        # print pubProj
        pubString = pub['Bibliografia']
        if pubString == None:
            pubString = 'blank'
        # try:
            # pubString = pub['Bibliografia']
        # except:
        newPub = Publication(name = pubString)
        newPub.save()
        try:
            proj = Project.objects.get(sigla = pubProj)
            proj.bibliografia.add(newPub)
            proj.save()
        except Exception, e:
            print e