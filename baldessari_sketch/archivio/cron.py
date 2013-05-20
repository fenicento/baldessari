from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
import json, os.path, re

# import models
from archivio.models import *


def create_jsons():
    
    projects = Project.objects.all().values_list('denominazione', flat=True)
    lol = os.path.join(os.path.dirname(os.path.realpath(__file__)),"projnames.json")
    with open(lol, 'w') as outfile:
        json.dump(list(projects), outfile)
        
        
        