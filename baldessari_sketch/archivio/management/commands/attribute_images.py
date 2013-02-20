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

def attributeImages(self):
    print "Starting imageAddress storing procedure"
    fichier = open(os.path.join(FILE_PATH, 'log_images.txt'), "w")
    
    drawings = Drawing.objects.all()
    letters = Letter.objects.all()
    
    for drawing in drawings:
        #raws = drawing.segnatura.split('_')
        folderAddress = DRAWS_PATH + drawing.sigla_archivio +"/" + drawing.project.sigla +"/"
        #sketchAddress = DRAWS_PATH +"Carteggi/" + drawing.project.sigla.lower() +"/"
        imgAttributed = False
        searched_begining = drawing.segnatura
        if os.path.exists(folderAddress):
            
            for file in os.listdir(folderAddress):
                if re.search(r'%s'%searched_begining, file) is not None:
                    drawing.imageAdress = 'img_documents/' + drawing.sigla_archivio +"/" + drawing.project.sigla +"/" + file
                    thumb =  drawing.sigla_archivio +"/" + drawing.project.sigla +"/" +"Thumbs/" + "THU_" + file.split(".")[0] + ".jpg"
                   
                    if os.path.isfile(os.path.join(DRAWS_PATH,thumb)):
                        print thumb
                        drawing.thumbAdress = 'img_documents/' + thumb
                        
                    imgAttributed = True
            if imgAttributed is False:
                drawing.imageAdress = 'img_documents/noimage.jpg'
                drawing.thumbAdress = 'img_documents/nothumb.jpg'
            drawing.save()
        else:
            drawing.imageAdress = 'img_documents/noimage.jpg'
            drawing.thumbAdress = 'img_documents/nothumb.jpg'
            drawing.save()
            
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
                    thumb =  "carteggi/" + letter.project.sigla.lower() +"/" +"Thumbs/" + "THU_" + file2.split(".")[0] + ".jpg"
                    
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
        
        
            
        # thumbfolderAddress = THB_DRAWS_PATH + '/' + raws[1]
        # if os.path.exists(thumbfolderAddress):
        #     imgAttributed = False
        #     searched_begining = raws[2]
        #     for file in os.listdir(thumbfolderAddress):
        #         if re.search(r'%s'%searched_begining, file) is not None:
        #             drawing.thumbAdress = 'img_thumbs/' + raws[1] + '/' + file
        #             imgAttributed = True
        #     if imgAttributed is False:
        #         drawing.thumbAdress = 'img_thumbs/noimage.jpg'
        #         fichier.write(drawing.segnatura+'\n')
        # else:
        #     drawing.thumbAdress = 'img_thumbs/noimage.jpg'
        #     fichier.write(drawing.segnatura+'\n')
        # drawing.save()
    fichier.close()
        

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        attributeImages(self)