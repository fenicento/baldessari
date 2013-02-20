from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
import os
import glob
import Image
import shutil
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DRAWS_PATH = os.path.join(FILE_PATH, '/Users/davide/Documents/Baldessari/source/progetto_django-nuovi_models/baldessari_sketch/media/img_documents/')
# DRAWS_PATH = os.path.join(FILE_PATH, '../../../media/img_documents')
# THB_DRAWS_PATH = os.path.join(FILE_PATH, '../../../media/img_thumbs')

def attributeLetters(self):
    
    fichier = open(os.path.join(FILE_PATH, 'log_images.txt'), "w")
    
    letters = Letter.objects.all()
            
    print "starting letters integration"  
    
          
    for letter in letters:
        print letter
        #raws = drawing.segnatura.split('_')
        #folderAddress = DRAWS_PATH + drawing.sigla_archivio +"/" + drawing.project.sigla +"/"
        sketchAddress = DRAWS_PATH +"carteggi/" + letter.project.sigla.lower() +"/"
        imgAttributed = False
        searched_begining = letter.segnatura
        print sketchAddress
        if os.path.exists(sketchAddress):    
            for file2 in os.listdir(sketchAddress):
                if re.search(r'%s'%searched_begining, file2) is not None:
                    letter.imageAdress = 'img_documents/' + "carteggi/" + letter.project.sigla.lower() +"/" + file2
                    thumb =  "carteggi/" + letter.project.sigla.lower() +"/" +"Thumbs/" + "THU_" + file.split(".")[0] + ".jpg"
                    
                    if os.path.isfile(os.path.join(DRAWS_PATH,thumb)):
                        print thumb
                        letter.thumbAdress = 'img_documents/' + thumb
                    
                    imgAttributed = True
            if imgAttributed is False:
                letter.imageAdress = 'img_documents/noimage.jpg'
                letter.thumbAdress = 'img_documents/nothumb.jpg'
            letter.save()
        else:
            letter.imageAdress = 'img_documents/noimage.jpg'
            letter.thumbAdress = 'img_documents/nothumb.jpg'
            letter.save()
    fichier.close()
        

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        attributeLetters(self)