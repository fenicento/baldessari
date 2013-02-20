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

FILE_PATH = '/Users/davide/Documents/Baldessari/Dataset/img_documents/'
DRAWS_PATH = '/Users/davide/Documents/Baldessari/Dataset/img_documents/'

imageRootFolder = "img_documents/"

polimiFolder = "img_polimi/"
casvaFolder = "img_casva/"

i = 0

drawings = Drawing.objects.all()
for drawing in drawings:

    i = i + 1
    try:
        raws = drawing.segnatura.split('_')
        polimiAddress = DRAWS_PATH + polimiFolder + raws[1]
        casvaAddress = DRAWS_PATH + casvaFolder + raws[1]

        if os.path.exists(polimiAddress):
            folderAddress = polimiAddress
            prefix = imageRootFolder + polimiFolder + raws[1] + '/'
        elif os.path.exists(casvaAddress):
            folderAddress = casvaAddress
            prefix = imageRootFolder + casvaFolder + raws[1] + '/'
        else:
            folderAddress = None

        if folderAddress is not None:
            imgAttributed = False
            searched_begining = raws[2]
            for file in os.listdir(folderAddress):
                if re.search(r'%s'%searched_begining, file) is not None:
                    drawing.imageAdress = prefix + file
                    # drawing.imageAdress = 'img_documents/' + raws[1] + '/' + file
                    imgAttributed = True
            if imgAttributed is False:
                drawing.imageAdress = 'img_documents/noimage.jpg'
        else:
            drawing.imageAdress = 'img_documents/noimage.jpg'

        drawing.save()
        print ("Immagine salvata: " + str(i))

    except Exception, e:
        print e


    # TODO: thumbnails!