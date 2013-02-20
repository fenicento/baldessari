from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(FILE_PATH, '../../../media/img_documents/ALB/')

def checkOrphanDocs(self):

    out_file = open("test.txt","w")
    
    i=0
    for root, dirs, files in os.walk(IMG_PATH):
        for name in files:
            if not name.startswith("THU_") and name.endswith((".jpeg", ".jpg",".png")):
                sign=name.split(".")[0]
                bitSign=sign.split("-")[0]
                try:
                    drawing = Drawing.objects.get(segnatura__startswith=bitSign)
                    print sign + "paired with" + drawing.segnatura
                except Exception, e:
                    print e
                    print sign + " is orphan"
                    i+=1
                    out_file.write(sign+"\n")
    print str(i)
    out_file.write(str(i) + " orphan documents found")
    out_file.close()
    
    

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        checkOrphanDocs(self)