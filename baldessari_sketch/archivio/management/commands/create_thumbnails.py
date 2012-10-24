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

def generateThumbnails(self):
    for dir in os.listdir(IMG_PATH):
        dirAddress = IMG_PATH+'/'+dir+'/'
        if os.path.isdir(dirAddress):
            #create dir
            dirT = THB_PATH+'/'+dir+'/'
            if not os.path.exists(dirT):
                os.makedirs(dirT)
            
            for file in os.listdir(dirAddress):
                path1 = dirAddress + "/" + file
                path2 = dirT + "/" + file
                if not os.path.exists(path2):
                    shutil.copyfile(path1, path2)
                im = Image.open(path2)
                im.thumbnail((120, 70), Image.ANTIALIAS)
                im.save(path2)

        

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        
        generateThumbnails(self)