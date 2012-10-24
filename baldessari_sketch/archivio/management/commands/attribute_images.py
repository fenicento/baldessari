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
IMG_PATH = os.path.join(FILE_PATH, '../../../static/img_documents')
THB_PATH = os.path.join(FILE_PATH, '../../../static/img_thumbs')

def attributeImages(self):
    fichier = open(os.path.join(FILE_PATH, 'log_images.txt'), "w")
    drawings = Drawing.objects.all()
    for drawing in drawings:
        raws = drawing.segnatura.split('_')
        folderAddress = IMG_PATH + '/' + raws[1]
        if os.path.exists(folderAddress):
            imgAttributed = False
            searched_begining = raws[2]
            for file in os.listdir(folderAddress):
                if re.search(r'%s'%searched_begining, file) is not None:
                    drawing.imageAdress = 'img_documents/' + raws[1] + '/' + file
                    imgAttributed = True
            if imgAttributed is False:
                drawing.imageAdress = 'img_documents/noimage.jpg'
        else:
            drawing.imageAdress = 'img_documents/noimage.jpg'
            
        thumbfolderAddress = THB_PATH + '/' + raws[1]
        if os.path.exists(thumbfolderAddress):
            imgAttributed = False
            searched_begining = raws[2]
            for file in os.listdir(thumbfolderAddress):
                if re.search(r'%s'%searched_begining, file) is not None:
                    drawing.thumbAdress = 'img_thumbs/' + raws[1] + '/' + file
                    imgAttributed = True
            if imgAttributed is False:
                drawing.thumbAdress = 'img_thumbs/noimage.jpg'
                fichier.write(drawing.segnatura+'\n')
        else:
            drawing.thumbAdress = 'img_thumbs/noimage.jpg'
            fichier.write(drawing.segnatura+'\n')
        drawing.save()
    fichier.close()
        

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        attributeImages(self)