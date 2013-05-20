# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
from StringIO import StringIO
import re
import os



def transferImages(self):
    
    themes = ThemeDetail.objects.all()
    
    for t in themes:
        img = t.imgUrl.split(".")[0]
        print t.titolo
        print img
        doc=None
        try:
            doc=Drawing.objects.filter(segnatura__icontains=img)[0]
        except:
            print "no doc found"
            try:
                doc=Letter.objects.filter(segnatura__icontains=img)[0]
            except:
                print "no letter found"
                
        if doc is not None:
            t.immagine=doc.imageAdress
            print t.immagine.url
            t.save()
            
        
        print "------------"
        
    bios = BioDetail.objects.all()
        
    for b in bios:
        
        print b.titolo
        
        
        if not "noimage" in b.imgUrl:
            b.immagine=b.imgUrl
            print b.immagine.url
            
        print "------------"
    

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        transferImages(self)