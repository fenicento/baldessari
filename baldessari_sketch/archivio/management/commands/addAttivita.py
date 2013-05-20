# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
from StringIO import StringIO
import re
import os

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"

def addActivities(self):

    file = open(os.path.join(FILE_PATH, 'activities.json'), 'r')
    docContent = StringIO(file.read())
    docDict = json.load(docContent)   #this dict will be updated with the content of docsDict
    file.close()
    
    # date variables
    
    for doc in docDict:
        print doc['segnatura']
        try:
            p = Drawing.objects.filter(segnatura__icontains = doc['segnatura'])[0]
            print ("doc esistente: " + doc['segnatura'])
            print ("attivita del json: " + doc['attivita'])
            p.attivita = doc['attivita']
            print p.attivita
            p.save()
            print "---------------"
    
        except Exception,e:     # doc does not exist
            print e
        
    

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        addActivities(self)