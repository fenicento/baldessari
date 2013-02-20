from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from archivio.models import *
from baldessari_sketch import settings
import datetime
import json
import re
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DRAWS_PATH = os.path.join(FILE_PATH, '/Users/davide/Documents/Baldessari/Dataset/immagini_di_scorta/Carteggi_jpeg/')

def insertCarteggi(self):
    
    #load values
    projects=Project.objects.all()
    letters=Letter.objects.all()
    times=TimeInterval.objects.all()
    
    #loop on all projects
    for p in projects:
        
        #check if a folder exists for the project
        currPath=DRAWS_PATH+p['sigla']
        if os.path.isdir(currPath):
            
            #take all files in the folder
            for cart in os.listdir(currPath):
                
                #retrieve signature from filename
                sign=os.path.splitext(cart)[0]
                
                #check if letter is already stored
                try:
                    newLetter = letters.get(segnatura = sign)
                
                #if letter is new, add it
                except:
                    newLetter = Letter(segnatura=sign, project=p)
                    
                    #assign the first beginning year of the project to the letter
                    for t in times:
                        if t.target == p:
                            newLetter.year=t.beginningYear
                            break
                            
                    #store the new letter
                    newLetter.save()
                    
                    