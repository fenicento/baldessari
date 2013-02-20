from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.core.management import call_command
from archivio.models import *
from baldessari_sketch import settings
import datetime, json, re
from StringIO import StringIO
from django.core.files import File
import os.path

FILE_PATH = "/Users/davide/Documents/Baldessari/Dataset/tabelle/json"

file = open(os.path.join(FILE_PATH, 'progetti_new.json'), 'r')
projContent = StringIO(file.read())
# projDict = json.load('[%s]' %  projContent[:-1])
projDict = json.load(projContent)   #this dict will be updated with the content of docsDict
file.close()

# Project.objects.all().delete()  

# date variables
datesSeparator = ';'
intervalSeparator = '-'

i = 0

for project in projDict:
    i = i+1
    #get or create project
    try:
        p = Project.objects.get(denominazione = project['denominazione'])
        print ("progetto esistente: " + str(i))

    except:     # project does not exist yet
        try:
            p = Project(sigla = project['sigla'])

            # 'denominazione' cannot be None - in case, use "blank"
            denom = project['denominazione']
            if denom != None:
                p.denominazione = denom
            else:
                p.denominazione = "blank"

            try:
                p.tipo = project['tipo_1']
                p.tipo2 = project['tipo_2 (tipologia SAN)']
            except:
                p.tipo = None
                p.tipo2 = None

            # geographical data
            p.address = project['indirizzo']
            try:
                lat = project['latitude']
                p.latitude = lat
                lgt = project['longitude']
                p.longitude = lgt
            except:
                p.latitude = None
                p.longitude = None

            # save in the database
            print p.sigla
            p.save()
            # print ("progetto salvato: " + str(i))

            # set date
            data = str(project['data'])
            try:
                nIntervals = data.count(datesSeparator) + 1     # number of date intervals
                # dates = []
                for interv in range(nIntervals):
                    leftData, separator, rightData = data.partition(datesSeparator)     # split string according to datesSeparator
                    data = rightData     # update data with the remaining part of the string
                    # dates.append(leftData)

                    if len(leftData) > 4:   # interval
                        dateA, sep, dateB = leftData.partition(intervalSeparator)
                    else:   # single year, e.g. len('1945') == 4
                        dateA = leftData
                        dateB = leftData  # begin and end correspond
                    # dates related to a project are set as Jan 1st of that year
                    dateBegin = datetime.date(int(dateA), 1,1)
                    dateEnd = datetime.date(int(dateB), 1,1)

                    try:    # already in the database
                        d = TimeInterval.get(
                            target = p, 
                            beginningDate = dateBegin,
                            beginningYear = dateBegin.year,
                            beginningMonth = None,
                            beginningDay = None,
                            endDate = dateEnd,
                            endYear = dateEnd.year,
                            endMonth = None,
                            endDay = None,
                            )

                    except: # not in the database
                        d = TimeInterval(
                            target = p, 
                            beginningDate = dateBegin,
                            beginningYear = dateBegin.year,
                            beginningMonth = None,
                            beginningDay = None,
                            endDate = dateEnd,
                            endYear = dateEnd.year,
                            endMonth = None,
                            endDay = None,
                            )
                        d.save()
            except Exception, e:
                print "Data is null"
                print e

                    

            # print(p.denominazione)



        except Exception, e:
            print "Exception: "
            print i
            print e
            # print ("non-denom")
            p.sigla = project['sigla']
            p.denominazione = "blank"
            p.tipo = None
            p.tipo2 = None
            p.address = None
            p.latitude = None
            p.longitude = None
            p.save()