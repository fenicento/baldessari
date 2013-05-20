from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"


def loadMartDocs(self):
    file = open(os.path.join(FILE_PATH, 'metadati_MART.json'), 'r')
    docContent = StringIO(file.read())
    docDict = json.load(docContent) #this dict will be updated with the content of docsDict
    file.close()
    
    # date variables
    dateSeparator = '/'
    
    i = 0
    
    #get or create project
    for doc in docDict:
        i = i+1
        try:
            d = Drawing.objects.get(segnatura = doc['segnatura'])
        except: # document not present
            segn = doc['segnatura']
            if segn is None:
                segn = 'blank'
            d = Drawing(segnatura = segn)
            try:
                d.project = Project.objects.get(sigla = doc['progetto'])
            except:
                d.project = None
            d.archivio = doc['sigla_archivio']
            #d.formato = doc['formato']
            d.annotazioni = doc['annotazioni']
            d.tecnica = doc['supporto']
            d.supporto = doc['supporto']
            d.tipo = doc['descrizione']
            d.segnatura = doc['segnatura']
            #d.strumento = doc['strumento']
            #d.scala = doc['scala']
            d.sigla_archivio = doc['sigla_archivio']
            #d.multipli = doc['multipli']
            #d.restauri = doc['restauri']
            #d.formato_cornice = doc['formato_cornice']
            #d.collocazione = doc['collocazione']
            #d.conservazione = doc['conservazione']
            #d.riproduzione = doc['riproduzione']
            #d.cartigli = doc['cartigli']
            # set date
            try:
                data = doc['data']
                prec = doc['precisione']
    
                day = ''
                month = ''
                year = ''
                dateDay = 0
                dateMonth = 0
                dateYear = 0
    
                if data is not None:
                    nDateElements = data.count(dateSeparator)
                    if nDateElements + 1 == 3:   # 3 date elements - i.e. dd/mm/yyyy
                        day, sep, rest = data.partition(dateSeparator)
                        month, sep, year = rest.partition(dateSeparator)
    
                        if prec == 'year':
                            day = '1'
                            dateDay = None
                            month = '1'
                            dateMonth = None
                        elif prec == 'month':
                            day = '1'
                            dateDay = None
                            dateMonth = int(month)
                        else:
                            dateDay = int(day)
                            dateMonth = int(month)
    
                        dateYear = int(year)
                        d.data = datetime.data(int(year), int(month), int(day))
                        d.dataDay = dateDay
                        d.dataMonth = dateMonth
                        d.dataYear = dateYear
            except Exception, e:
                # print e
                d.data = None
                d.dateDay = None
                d.dateMonth = None
                d.dateYear = None
            d.save()
            print ("documento salvato: " + str(i))
        
        
class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        loadMartDocs(self)