from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
from StringIO import StringIO
from django.core.files import File
import os.path


def load_bio(self):

    FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"
    
    file = open(os.path.join(FILE_PATH, 'bio.json'), 'r')
    bioContent = StringIO(file.read())
    bioDict = json.load(bioContent) #this dict will be updated with the content of docsDict
    file.close()
    
    BioDetail.objects.all().delete()

    
    for pub in bioDict:     # for each biodetail

        try:
            p = BioDetail.objects.get(titolo = pub['TITOLO'])
        except:
            newBio=BioDetail(titolo=pub['TITOLO'])
            newBio.didascalia=pub['DIDASCALIA']
            newBio.testo=pub['TESTO']
            
            if '-' in pub['DATA']:
                dates=pub['DATA'].split('-')
                newBio.startDate=int(float(dates[0]))
                newBio.endDate=int(float(dates[1]))
            else:
                newBio.startDate=int(float(pub['DATA']))
                newBio.endDate=int(float(pub['DATA']))
            
            if pub['IMMAGINE'] is not None:
                imgs=Drawing.objects.filter(segnatura__icontains=pub['IMMAGINE'])
                if imgs:
                    newBio.imgUrl=imgs[0].imageAdress
                else:
                    imgs=Letter.objects.filter(segnatura__icontains=pub['IMMAGINE'])
                    if imgs:
                        newBio.imgUrl=imgs[0].imageAdress
                    else: 
                        newBio.imgUrl='img_documents/noimage.jpg'
            else:
                newBio.imgUrl='img_documents/noimage.jpg'
                    
            newBio.save()
            


class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        load_bio(self)