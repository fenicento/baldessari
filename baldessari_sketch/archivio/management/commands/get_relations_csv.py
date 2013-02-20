import csv
from StringIO import StringIO
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import os.path
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Create csv file containing relations between Baldessari and actors
# Including project, actor and role

# (After db is created)

def get_relation_csv(self):
    file = open(os.path.join(FILE_PATH, 'relazioni.csv'), 'wb+')
    output = csv.writer(file)
    
    values = [
                  "sigla progetto",
                  "nome del' attore",
                  "tipo di relazione"
                  ]    
    output.writerow(values)


    Relazione = Participation.objects.all()
    
    for part in Relazione: 
        project = part.project.denominazione.encode('latin-1')
        actor = part.actor.name.encode('latin-1')
        ruolo = part.role.encode('latin-1')
        
        '''
        if(ruolo == 'COL'): 
            ruolo = 'collaboratore'
        elif(ruolo == 'COP'): 
            ruolo = "coprogettista"
        else :
            ruolo = 'comittente'
        '''
        
        
        values = [
                  project,
                  actor,
                  ruolo
                  ]    
        
        
        output.writerow(values) 

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        get_relation_csv(self)