'''
This script gives automatically a date to all publications objects, extracting from the raw String a number that looks like a year
'''


from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re

cherchedate = r"19([0-9]){2}"
cherchecomp = re.compile(cherchedate)

def giveDate(self):
    Pubs = Publication.objects.all()
    for pub in Pubs:
        nom = pub.name.encode("latin-1")
        if cherchecomp.search(nom) is not None:
            year = cherchecomp.search(nom).group(0)
            date = datetime.datetime(int(year), 1, 1, 0, 0, 0, 0)
            pub.date = date
            pub.save()
        

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        giveDate(self)